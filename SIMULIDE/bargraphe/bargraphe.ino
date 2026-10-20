void setup() {
	for (int pin=3;pin<=12;pin++){
		pinMode(pin, OUTPUT);
	}
}

void loop() {
	for (int pin=3;pin<=12;pin++){
		digitalWrite(pin, HIGH);
		delay(100);
		digitalWrite(pin, LOW);
	}
}