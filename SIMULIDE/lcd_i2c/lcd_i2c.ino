#include <LiquidCrystal_AIP31068_I2C.h>

// adresse I2C de l'afficheur, nombre de colonnes, nombre de lignes
LiquidCrystal_AIP31068_I2C lcd(0x3E, 16, 2);

void setup() {
  lcd.init();
  lcd.setCursor(1, 0);     // colonne 1, ligne 0 (1re ligne)
  lcd.print("HELLO");
  lcd.setCursor(8, 1);     // colonne 8, ligne 1 (2e ligne)
  lcd.print("WORLD");

}

void loop(){
}