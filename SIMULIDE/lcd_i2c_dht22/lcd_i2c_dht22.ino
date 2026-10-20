#include <DHT.h>
#include <LiquidCrystal_AIP31068_I2C.h>

LiquidCrystal_AIP31068_I2C lcd(0x3E, 16, 2);

#define PIN_DHT A0       // broche où est branchée la sortie du DHT22
#define TYPE_DHT DHT22

DHT dht(PIN_DHT, TYPE_DHT);

void setup() {
  lcd.init();
  dht.begin();
  lcd.setCursor(1, 0);     // colonne 1, ligne 0 (1re ligne)
  lcd.print("IMT NE - PPI");

}

void loop(){
	delay(2000);
	float temp = dht.readTemperature();
	float hum = dht.readHumidity();
	lcd.setCursor(0, 1);
	lcd.print("T ");
	lcd.print(temp, 1);
	lcd.print("oC/H ");
	lcd.print(hum, 1);
	lcd.print("%");
	
	
	
}