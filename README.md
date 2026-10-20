# Projet IoT - iot_by

## Présentation
Ce dépôt regroupe les fichiers et les travaux du projet IoT « Création d'un capteur de température et d'humidité » (IMT Nord Europe - PPI).
Le projet final est le capteur IdO **TempHumiX**, simulé sous SimulIDE avec une carte Arduino Uno.

## Objectifs
- Organiser les sources et les ressources du projet.
- Conserver l'historique des modifications avec Git.
- Synchroniser le travail avec GitHub.

## Organisation du dépôt
- `README.md` : présentation du projet et consignes.
- `.gitignore` : fichiers exclus du suivi Git (fichiers compilés, temporaires...).
- `SIMULIDE/` : circuits (`.sim1`) et programmes Arduino (`.ino`) de chaque exercice.

| Dossier | Description |
|---|---|
| `SIMULIDE/clignotement_led/` | LED qui clignote sur la broche 2 (500 ms) |
| `SIMULIDE/bargraphe/` | Chenillard sur un bargraphe de 10 LED (100 ms) |
| `SIMULIDE/capteur_dht22/` | LED verte si température < 20 °C, sinon LED rouge |
| `SIMULIDE/lcd_i2c/` | Affichage « HELLO WORLD » sur un LCD 16x2 I2C |
| `SIMULIDE/lcd_i2c_dht22/` | Affichage de la température et de l'humidité sur le LCD |
| `SIMULIDE/TempHumiX/` | Capteur final : LED de vie, dateur, DHT22, LCD et port série |

## Fonctionnement de TempHumiX
- LED de vie qui clignote à 2 Hz.
- Lecture de la température et de l'humidité (DHT22) toutes les 2000 ms.
- Dateur (seconde, minute, heure, jour, mois, année ; mois de 30 jours).
- Ligne 1 du LCD : date et heure. Ligne 2 : température et humidité (au dixième).
- Envoi de la date, de l'heure et des mesures sur le port série (9600 bauds).
- Structure du programme : une boucle de 100 ms avec un compteur pour cadencer les tâches.

## Branchements principaux (Arduino Uno)
- DHT22 : données sur A0
- LCD I2C : SDA sur A4, SCL sur A5
- Port série : TX (1) vers Rx, RX (0) vers Tx
- LED de vie : broche 2

## Prérequis
- Git
- Arduino IDE 1.8.19
- SimulIDE 1.1.0
- Bibliothèques Arduino :
  - DHT sensor library (Adafruit) + Adafruit Unified Sensor
  - LiquidCrystal AIP31068 (inclure `LiquidCrystal_AIP31068_I2C.h`)

## Utilisation
1. Cloner le dépôt ou récupérer les fichiers.
2. Ouvrir le circuit `.sim1` d'un exercice dans SimulIDE.
3. Ouvrir le fichier `.ino` correspondant, puis le compiler.
4. Charger le fichier `.hex` dans l'Arduino (clic droit → Charger firmware).
5. Lancer la simulation.