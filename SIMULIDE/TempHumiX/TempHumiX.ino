#include <WiFiS3.h>

#define VERSION "V1.0"

// pour tester le 5G : mettre la ligne 2,4 GHz en commentaire
char ssid[] = "IoT IMT Nord Europe";       // 2,4 GHz
//char ssid[] = "IoT IMT Nord Europe 5G";  // 5 GHz
char pass[] = "72Hin@R*";

#include <Wire.h>
#include <DHT.h>
#include <NTPClient.h>
#include "rgb_lcd.h"
#include "RTC.h"

#define PIN_DHT A0 // broche du DHT22
#define TYPE_DHT DHT22
#define PIN_VIE 2 // led de vie
#define DECALAGE_HORAIRE 7200 //declage horaire heure de paris +2h

rgb_lcd lcd;
DHT dht(PIN_DHT, TYPE_DHT);

WiFiUDP ntpUDP;
NTPClient ntp(ntpUDP, "192.168.1.254", DECALAGE_HORAIRE);

bool ntpOk=false; // true si la derniere synchro a reussi

unsigned long compteur=0; // 1 tour de loop = 500 ms

int etatVie=LOW;
float temp=0;
float hum=0;

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
void setup() {
  Serial.begin(9600);
  pinMode(PIN_VIE, OUTPUT);
  lcd.begin(16,2);
  dht.begin();
  RTC.begin();
  RTCTime depart(21, Month::OCTOBER, 2026, 14, 0, 0, DayOfWeek::WEDNESDAY, SaveLight::SAVING_TIME_INACTIVE);
  RTC.setTime(depart);
  bool wifiOk = setup_wifi();
  ntp.begin();
  ntpOk = synchro_ntp();

  // ecran d'accueil : version + date, puis adresse IP
  RTCTime maintenant;
  RTC.getTime(maintenant);

  // ligne 1 LCD + port serie : version et date
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

  // ligne 2 LCD + port serie : adresse IP
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
  lcd.clear();
}

void loop(){
  delay(500);
  compteur++;

  // led de vie : change d'etat a chaque tour (500 ms)
  if (etatVie==LOW){
    etatVie=HIGH;
  }else{
    etatVie=LOW;
  }
  digitalWrite(PIN_VIE, etatVie);

  if (compteur%120==0){
  ntpOk = synchro_ntp();
  }

  // date et heure toutes les 1000 ms = 2 tours
  if (compteur%2==0){
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

  // mesure toutes les 2000 ms = 4 tours
  if (compteur%4==0){
    float t = dht.readTemperature();
    float h = dht.readHumidity();
    if (!isnan(t) && !isnan(h)){
      temp=t;
      hum=h;
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