#include <DHT.h>
#include <LiquidCrystal_AIP31068_I2C.h>

#define PIN_DHT A0 // broche du DHT22
#define TYPE_DHT DHT22
#define PIN_VIE 2 // led de vie

LiquidCrystal_AIP31068_I2C lcd(0x3E, 16, 2);
DHT dht(PIN_DHT, TYPE_DHT);

unsigned long compteur=0; // 1 tour de loop = 100 ms

// date de depart
int sec=0;
int minu=0;
int heure=12;
int jour=1;
int mois=1;
int annee=26;

float temp=0;
float hum=0;

void setup() {
Serial.begin(9600);
pinMode(PIN_VIE, OUTPUT);
lcd.init();
dht.begin();
}

void loop(){
delay(100);
compteur++;

// led de vie 2Hz (periode 500ms = 5 tours)
if (compteur%5<2){
digitalWrite(PIN_VIE, HIGH);
}else{
digitalWrite(PIN_VIE, LOW);
}

// dateur : 1 seconde = 10 tours
if (compteur%10==0){
sec++;
if (sec>=60){
sec=0;
minu++;
}
if (minu>=60){
minu=0;
heure++;
}
if (heure>=24){
heure=0;
jour++;
}
if (jour>30){
jour=1;
mois++;
}
if (mois>12){
mois=1;
annee++;
}
}

// mesure toutes les 2000 ms = 20 tours
if (compteur%20==0){
float t = dht.readTemperature();
float h = dht.readHumidity();
if (!isnan(t) && !isnan(h)){
temp=t;
hum=h;
}

// envoi sur le port serie
Serial.print(jour);
Serial.print("/");
Serial.print(mois);
Serial.print("/");
Serial.print(annee);
Serial.print(" ");
if (heure<10) Serial.print("0");
Serial.print(heure);
Serial.print(":");
if (minu<10) Serial.print("0");
Serial.print(minu);
Serial.print(":");
if (sec<10) Serial.print("0");
Serial.print(sec);
Serial.print(" T ");
Serial.print(temp, 1);
Serial.print("oC/H ");
Serial.print(hum, 1);
Serial.println("%");
}

// ligne 1 : date et heure
lcd.setCursor(0, 0);
lcd.print(jour);
lcd.print("/");
lcd.print(mois);
lcd.print("/");
lcd.print(annee);
lcd.print(" ");
if (heure<10) lcd.print("0");
lcd.print(heure);
lcd.print(":");
if (minu<10) lcd.print("0");
lcd.print(minu);
lcd.print(":");
if (sec<10) lcd.print("0");
lcd.print(sec);
lcd.print("  ");

// ligne 2 : temperature et humidite
lcd.setCursor(0, 1);
lcd.print("T ");
lcd.print(temp, 1);
lcd.print("oC/H ");
lcd.print(hum, 1);
lcd.print("%  ");
}