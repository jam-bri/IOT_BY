#include <WiFiS3.h>

#define VERSION "V1.0"

// pour tester le 5G : mettre la ligne 2,4 GHz en commentaire
char ssid[] = "IoT IMT Nord Europe";       // 2,4 GHz
//char ssid[] = "IoT IMT Nord Europe 5G";  // 5 GHz
char pass[] = "72Hin@R*";
char username[] = "mos_user";
char mdp[] = "mos_user";
char idCap[] = "IdO_Client_42914";

#include <Wire.h>
#include <DHT.h>
#include <NTPClient.h>
#include "rgb_lcd.h"
#include "RTC.h"
#include <ArduinoMqttClient.h>

#define PIN_DHT A0 // broche du DHT22
#define TYPE_DHT DHT22
#define PIN_VIE 2 // led de vie
#define PIN_BAR_DEBUT 3 // 1re broche du bargraphe (A VERIFIER sur le schema)
#define NB_BARRES 10 // nombre de barres
#define DECALAGE_HORAIRE 7200 // decalage horaire heure de paris +2h
#define PORT 1883
#define IP_HOST "192.168.1.1"
#define ID_CAP "42914"

// periodes de la led de vie en ms
#define PERIODE_NORMALE 500 // 2 Hz
#define PERIODE_LENTE 2000
#define PERIODE_RAPIDE 200

rgb_lcd lcd;
DHT dht(PIN_DHT, TYPE_DHT);

WiFiUDP ntpUDP;
NTPClient ntp(ntpUDP, "192.168.1.254", DECALAGE_HORAIRE);
WiFiClient wifiClient;
MqttClient mqttClient(wifiClient);

bool ntpOk=false; // true si la derniere synchro a reussi
bool mesureActive=true; // false apres la commande 30
int mqttErreur=-1; // 0 si connecte au broker

unsigned long compteur=0; // 1 tour de loop = 100 ms

int periodeVie=PERIODE_NORMALE; // periode actuelle de la led de vie
int periodePerso=1000; // periode recue sur BLINK_

float temp=0;
float hum=0;

// dernieres valeurs publiees, en dixiemes (-9999 = rien publie encore)
int tempPubliee=-9999;
int humPubliee=-9999;

// topics publies
String topicVersion = String("/iot/VERSION_") + ID_CAP;
String topicTemperature = String("/iot/TEMPERATURE_") + ID_CAP;
String topicHumidity = String("/iot/HUMIDITY_") + ID_CAP;
String topicDate = String("/iot/GET_DATE_") + ID_CAP;

// topics souscrits
String topicCommand = String("/iot/COMMAND_") + ID_CAP;
String topicBargraph = String("/iot/BARGRAPH_") + ID_CAP;
String topicBlink = String("/iot/BLINK_") + ID_CAP;

bool setup_wifi(){
  Serial.print("Connexion a ");
  Serial.println(ssid);
  WiFi.begin(ssid, pass);

  // on attend la connexion, 10 s maximum (20 x 500 ms)
  int essais=0;
  while (WiFi.status()!=WL_CONNECTED && essais<20){
    delay(500);
    Serial.print(".");
    essais++;
  }
  Serial.println();

  if(WiFi.status()==WL_CONNECTED){
    // l'adresse IP peut arriver un peu apres la connexion
    while (WiFi.localIP()==IPAddress(0,0,0,0)){
      delay(100);
    }
    Serial.print("Connecte, IP : ");
    Serial.println(WiFi.localIP());
    return true;
  }else{
    Serial.println("Echec connexion wifi");
    return false;
  }
}

// synchro de l'heure avec le serveur NTP, renvoie true si ok
bool synchro_ntp(){
  if (WiFi.status()!=WL_CONNECTED){
    return false;
  }
  if (ntp.update()){
    RTCTime heureNTP(ntp.getEpochTime());
    RTC.setTime(heureNTP);
    Serial.println("Synchro NTP ok");
    return true;
  }
  Serial.println("Echec synchro NTP");
  return false;
}

int setup_mqtt(){
  Serial.println("Connexion au broker MQTT");

  mqttClient.setId(idCap); // identifiant du capteur
  mqttClient.setUsernamePassword(username, mdp); // identifiants du broker

  if (!mqttClient.connect(IP_HOST, PORT)) {
    Serial.println("Echec connexion MQTT");
    return mqttClient.connectError(); // code d'erreur MQTT
  }else{
    Serial.println("Connecte au broker");
    return 0;
  }
}

// publie la version (format X.Y)
void publier_version(){
  mqttClient.beginMessage(topicVersion);
  mqttClient.print(1.0, 1);
  mqttClient.endMessage();
  Serial.println("Version publiee");
}

// publie temperature, humidite et date
void publier_mesures(float temp, float hum){
  // temperature au dixieme
  mqttClient.beginMessage(topicTemperature);
  mqttClient.print(temp, 1);
  mqttClient.endMessage();

  // humidite au dixieme
  mqttClient.beginMessage(topicHumidity);
  mqttClient.print(hum, 1);
  mqttClient.endMessage();

  // date au format JJ/MM/AAAA HH:MM:SS
  RTCTime maintenant;
  RTC.getTime(maintenant);
  char texte[20];
  sprintf(texte, "%02d/%02d/%04d %02d:%02d:%02d",
          maintenant.getDayOfMonth(),
          Month2int(maintenant.getMonth()),
          maintenant.getYear(),
          maintenant.getHour(),
          maintenant.getMinutes(),
          maintenant.getSeconds());
  mqttClient.beginMessage(topicDate);
  mqttClient.print(texte);
  mqttClient.endMessage();

  Serial.println("Mesures publiees");
}

// allume un nombre de barres proportionnel a la valeur (0 a 1023)
void afficher_bargraphe(int valeur){
  int nbAllumees = map(valeur, 0, 1023, 0, NB_BARRES); // 0..1023 -> 0..10
  for (int i=0;i<NB_BARRES;i++){
    if (i<nbAllumees){
      digitalWrite(PIN_BAR_DEBUT+i, HIGH);
    }else{
      digitalWrite(PIN_BAR_DEBUT+i, LOW);
    }
  }
}

// traite un code de commande recu sur COMMAND_
void traiter_commande(int code){
  if (code==10){
    ntpOk = synchro_ntp(); // forcer la mise a l'heure
    if (ntpOk){
      publier_version(); // 6.1.6 a : version publiee seulement apres synchro NTP
    }
  }else if (code==20){
    mesureActive=true; // demarrage mesure
  }else if (code==30){
    mesureActive=false; // arret mesure
  }else if (code==40){
    periodeVie=PERIODE_LENTE; // clignotement lent
  }else if (code==50){
    periodeVie=PERIODE_RAPIDE; // clignotement rapide
  }else if (code==60){
    periodeVie=periodePerso; // clignotement personnalise
  }else{
    Serial.println("Code commande inconnu");
  }
}

// appelee automatiquement a la reception d'un message MQTT
void onMqttMessage(int tailleMessage){
  // acquisition du topic
  String topic = mqttClient.messageTopic();

  // acquisition du message
  String message = "";
  while (mqttClient.available()){
    message += (char)mqttClient.read();
  }

  // conversion du message en entier
  int valeur = message.toInt();

  Serial.print("Recu sur ");
  Serial.print(topic);
  Serial.print(" : ");
  Serial.println(valeur);

  if (topic.indexOf("COMMAND")>=0){
    traiter_commande(valeur);
  }else if (topic.indexOf("BARGRAPH")>=0){
    if (valeur<0) valeur=0;
    if (valeur>1023) valeur=1023;
    afficher_bargraphe(valeur);
  }else if (topic.indexOf("BLINK")>=0){
    // la periode doit etre un multiple de 100 ms
    valeur = (valeur/100)*100;
    if (valeur<200) valeur=200; // au moins 2 tours pour voir allume et eteint
    periodePerso=valeur;
    if (periodeVie!=PERIODE_NORMALE && periodeVie!=PERIODE_LENTE && periodeVie!=PERIODE_RAPIDE){
      periodeVie=periodePerso; // si on est deja en mode perso, on applique tout de suite
    }
  }
}

void setup() {
  Serial.begin(9600);
  while (!Serial && millis()<3000);
  pinMode(PIN_VIE, OUTPUT);
  for (int i=0;i<NB_BARRES;i++){
    pinMode(PIN_BAR_DEBUT+i, OUTPUT);
  }
  lcd.begin(16,2);
  dht.begin();
  RTC.begin();
  RTCTime depart(21, Month::OCTOBER, 2026, 14, 0, 0, DayOfWeek::WEDNESDAY, SaveLight::SAVING_TIME_INACTIVE);
  RTC.setTime(depart);
  bool wifiOk = setup_wifi();
  ntp.begin();
  ntpOk = synchro_ntp();
  mqttErreur = setup_mqtt();
  Serial.print("Code MQTT : ");
  Serial.println(mqttErreur);

  // souscription aux 3 topics si connecte
  if (mqttErreur==0){
    mqttClient.onMessage(onMqttMessage);
    mqttClient.subscribe(topicCommand);
    mqttClient.subscribe(topicBargraph);
    mqttClient.subscribe(topicBlink);
    Serial.println("Abonne a COMMAND, BARGRAPH et BLINK");
  }

  // ecran d'accueil : version + date, puis adresse IP
  RTCTime maintenant;
  RTC.getTime(maintenant);

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(VERSION);
  lcd.print("  ");
  Serial.print(VERSION);
  Serial.print("  ");

  if (maintenant.getDayOfMonth()<10){
    lcd.print("0");
    Serial.print("0");
  }
  lcd.print(maintenant.getDayOfMonth());
  lcd.print("/");
  Serial.print(maintenant.getDayOfMonth());
  Serial.print("/");

  if (Month2int(maintenant.getMonth())<10){
    lcd.print("0");
    Serial.print("0");
  }
  lcd.print(Month2int(maintenant.getMonth()));
  lcd.print("/");
  lcd.print(maintenant.getYear());
  Serial.print(Month2int(maintenant.getMonth()));
  Serial.print("/");
  Serial.println(maintenant.getYear());

  lcd.setCursor(0, 1);
  if (wifiOk){
    lcd.print(WiFi.localIP());
    Serial.print("IP : ");
    Serial.println(WiFi.localIP());
  }else{
    lcd.print("Pas de wifi");
    Serial.println("Pas de wifi");
  }
  delay(3000); // ecran d'accueil 3 s

  // 2e ecran d'accueil : etat MQTT
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("MQTT :");
  lcd.setCursor(0, 1);
  if (mqttErreur==0){
    lcd.print("Connecte");
  }else{
    lcd.print("Erreur ");
    lcd.print(mqttErreur);
  }
  delay(3000);
  lcd.clear();
}

void loop(){
  delay(100);
  compteur++;
  mqttClient.poll(); // garde la connexion et recoit les messages

  // led de vie : allumee la 1re moitie de la periode, eteinte la 2e
  int toursPeriode = periodeVie/100;
  if (compteur%toursPeriode < toursPeriode/2){
    digitalWrite(PIN_VIE, HIGH);
  }else{
    digitalWrite(PIN_VIE, LOW);
  }

  // resynchro NTP toutes les 60 s = 600 tours
  if (compteur%600==0){
    ntpOk = synchro_ntp();
  }

  // date et heure toutes les 1000 ms = 10 tours
  if (compteur%10==0){
    lcd.setCursor(0, 0);
    if (ntpOk){
      RTCTime maintenant;
      RTC.getTime(maintenant);
      lcd.print(maintenant.getDayOfMonth());
      lcd.print("/");
      lcd.print(Month2int(maintenant.getMonth()));
      lcd.print("/");
      lcd.print(maintenant.getYear()%100);
      lcd.print(" ");
      if (maintenant.getHour()<10) lcd.print("0");
      lcd.print(maintenant.getHour());
      lcd.print(":");
      if (maintenant.getMinutes()<10) lcd.print("0");
      lcd.print(maintenant.getMinutes());
      lcd.print(":");
      if (maintenant.getSeconds()<10) lcd.print("0");
      lcd.print(maintenant.getSeconds());
      lcd.print("  ");
    }else{
      lcd.print("Pas de synchro  ");
    }
  }

  // mesure toutes les 2000 ms = 20 tours (si mesure active)
  if (compteur%20==0 && mesureActive){
    float t = dht.readTemperature();
    float h = dht.readHumidity();
    if (!isnan(t) && !isnan(h)){
      temp=t;
      hum=h;
    }

    // 6.1.6 b : on ne publie que si la temperature ou l'humidite a change (au dixieme)
    int tempDixiemes = round(temp*10);
    int humDixiemes = round(hum*10);
    if (mqttErreur==0 && (tempDixiemes!=tempPubliee || humDixiemes!=humPubliee)){
      publier_mesures(temp, hum);
      tempPubliee=tempDixiemes;
      humPubliee=humDixiemes;
    }

    // envoi sur le port serie
    Serial.print("T ");
    Serial.print(temp, 1);
    Serial.print("oC/H ");
    Serial.print(hum, 1);
    Serial.println("%");

    // ligne 2 : temperature et humidite
    lcd.setCursor(0, 1);
    lcd.print("T ");
    lcd.print(temp, 1);
    lcd.print("oC/H ");
    lcd.print(hum, 1);
    lcd.print("%  ");
  }
}