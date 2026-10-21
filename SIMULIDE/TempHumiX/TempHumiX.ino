#include <WiFiS3.h>

#define VERSION "V1.0"

// pour tester le 5G : mettre la ligne 2,4 GHz en commentaire
char ssid[] = "IoT IMT Nord Europe";       // 2,4 GHz
//char ssid[] = "IoT IMT Nord Europe 5G";  // 5 GHz
char pass[] = "72Hin@R*";

#include <Wire.h>
#include <DHT.h>
#include "rgb_lcd.h"
#include "RTC.h"

#define PIN_DHT A0 // broche du DHT22
#define TYPE_DHT DHT22
#define PIN_VIE 2 // led de vie

rgb_lcd lcd;
DHT dht(PIN_DHT, TYPE_DHT);



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

void setup() {
  Serial.begin(9600);
  pinMode(PIN_VIE, OUTPUT);
  lcd.begin(16,2);
  dht.begin();
  RTC.begin();
  RTCTime depart(21, Month::OCTOBER, 2026, 14, 0, 0, DayOfWeek::WEDNESDAY, SaveLight::SAVING_TIME_INACTIVE);
  RTC.setTime(depart);
  bool wifiOk = setup_wifi();

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
}