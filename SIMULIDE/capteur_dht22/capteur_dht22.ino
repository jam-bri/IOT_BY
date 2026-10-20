#include <DHT.h>

#define PIN_DHT A0       // broche où est branchée la sortie du DHT22
#define TYPE_DHT DHT22

#define PIN_V 3
#define PIN_R 12

DHT dht(PIN_DHT, TYPE_DHT);

void setup() {
	dht.begin();
	pinMode(PIN_V, OUTPUT);
	pinMode(PIN_R, OUTPUT);
}

void loop() {
	delay(2000);
	float temperature = dht.readTemperature();
	if (temperature<20){
		digitalWrite(PIN_R, LOW);
		digitalWrite(PIN_V, HIGH);
	}else{
		digitalWrite(PIN_V, LOW);
		digitalWrite(PIN_R, HIGH);
	}
}