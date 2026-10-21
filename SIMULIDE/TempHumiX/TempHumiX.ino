#include <Wire.h>
#include <DHT.h>
#include "rgb_lcd.h"
#include "RTC.h"

#define PIN_DHT A0 // broche du DHT22
#define TYPE_DHT DHT22
#define PIN_VIE 2 // led de vie

rgb_lcd lcd;
DHT dht(PIN_DHT, TYPE_DHT);

unsigned long compteur=0; // 1 tour de loop = 100 ms

int etatVie=LOW;
float temp=0;
float hum=0;

void setup() {
  Serial.begin(9600);
  pinMode(PIN_VIE, OUTPUT);
  lcd.begin(16,2);
  dht.begin();
  RTC.begin();
  RTCTime depart(21, Month::OCTOBER, 2026, 11, 0, 0, DayOfWeek::WEDNESDAY, SaveLight::SAVING_TIME_INACTIVE);
  RTC.setTime(depart);
}

void loop(){
  delay(500);
  compteur++;

  // led de vie 2Hz (periode 500ms = 5 tours)
  if (etatVie==LOW){
    etatVie=HIGH;
  }else{
    etatVie=LOW;
  }
  digitalWrite(PIN_VIE, etatVie);
  // date et heure toutes les 1000 ms = 2 tours
  if (compteur%2==0){
    RTCTime maintenant;
    RTC.getTime(maintenant);
    lcd.setCursor(0, 0);
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
    Serial.print(" T ");
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