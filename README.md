# Projet IoT — TempHumiX

Projet IoT « Création d'un capteur de température et d'humidité ».

Le dépôt suit la construction progressive du capteur IdO **TempHumiX** :

1. **Simulation** sous SimulIDE avec une carte Arduino Uno : une série d'exercices (LED, bargraphe, DHT22, LCD I2C) qui mènent à un premier TempHumiX autonome.
2. **TP pratique** sur une carte réelle **Arduino UNO R4 WiFi** : TempHumiX devient un objet connecté (RTC, WiFi, synchronisation NTP, client MQTT pilotable à distance).

## Sommaire
- [Branches](#branches)
- [Arborescence](#arborescence)
- [Exercices de simulation](#exercices-de-simulation)
- [TempHumiX — version connectée](#temphumix--version-connectée)
- [Prérequis](#prérequis)
- [Utilisation](#utilisation)
- [Historique du projet](#historique-du-projet)

## Branches

| Branche | Contenu |
|---|---|
| `main` | Branche principale (actuellement au niveau de `simulation`) |
| `simulation` | Exercices SimulIDE et TempHumiX simulé (Arduino Uno) |
| `tp_pratique` | TempHumiX connecté sur UNO R4 WiFi (RTC, WiFi, NTP, MQTT) |

## Arborescence

```text
IOT_BY/
├── .gitignore                  # fichiers exclus (temporaires, secrets, .hex/.elf/.bin...)
├── README.md
├── SIMULIDE/                   # Partie 1 : simulation (Arduino Uno sous SimulIDE)
│   ├── clignotement_led/
│   │   ├── clignotement_led.ino
│   │   └── clignotement_led.sim1
│   ├── bargraphe/
│   │   ├── bargraphe.ino
│   │   └── bargraphe.sim1
│   ├── capteur_dht22/
│   │   ├── capteur_dht22.ino
│   │   └── capteur_dht22.sim1
│   ├── lcd_i2c/
│   │   ├── lcd_i2c.ino
│   │   └── lcd_i2c.sim1
│   ├── lcd_i2c_dht22/
│   │   ├── lcd_i2c_dht22.ino
│   │   └── lcd_i2c_dht22.sim1
│   └── TempHumiX/
│       ├── TempHumiX.ino       # TempHumiX simulé (Uno : LED de vie, dateur, DHT22, LCD, série)
│       └── TempHumiX.sim1      # circuit SimulIDE correspondant
└── TP_PRATIQUE/                # Partie 2 : carte réelle Arduino UNO R4 WiFi
    └── TempHumiX/
        └── TempHumiX.ino       # TempHumiX connecté (RTC, WiFi, NTP, MQTT)
```

Dans `SIMULIDE/`, chaque dossier contient un circuit SimulIDE (`.sim1`) et le programme Arduino (`.ino`) associé. `TP_PRATIQUE/` ne contient que du code : il se téléverse sur la carte réelle.

## Exercices de simulation

| Exercice | Objectif | Broches | Bibliothèques |
|---|---|---|---|
| [clignotement_led](SIMULIDE/clignotement_led/clignotement_led.ino) | LED qui clignote (500 ms allumée / 500 ms éteinte) | LED : 2 | — |
| [bargraphe](SIMULIDE/bargraphe/bargraphe.ino) | Chenillard sur un bargraphe de 10 LED (100 ms par LED) | 3 → 12 | — |
| [capteur_dht22](SIMULIDE/capteur_dht22/capteur_dht22.ino) | Toutes les 2 s : LED verte si T < 20 °C, sinon LED rouge | DHT22 : A0, verte : 3, rouge : 12 | DHT |
| [lcd_i2c](SIMULIDE/lcd_i2c/lcd_i2c.ino) | Affiche « HELLO » / « WORLD » sur un LCD 16x2 I2C (adresse `0x3E`) | SDA : A4, SCL : A5 | LiquidCrystal AIP31068 |
| [lcd_i2c_dht22](SIMULIDE/lcd_i2c_dht22/lcd_i2c_dht22.ino) | Ligne 1 : « IMT NE - PPI », ligne 2 : température et humidité au dixième | DHT22 : A0, LCD I2C | DHT, LiquidCrystal AIP31068 |
| [TempHumiX](SIMULIDE/TempHumiX/TempHumiX.ino) | TempHumiX simulé : LED de vie, dateur logiciel, mesure DHT22, affichage LCD et port série | LED de vie : 2, DHT22 : A0, LCD I2C | DHT, LiquidCrystal AIP31068 |

## TempHumiX — version connectée

> Programme : [TP_PRATIQUE/TempHumiX/TempHumiX.ino](TP_PRATIQUE/TempHumiX/TempHumiX.ino), pour la carte réelle **UNO R4 WiFi**. Il reprend le TempHumiX simulé ([SIMULIDE/TempHumiX](SIMULIDE/TempHumiX/)) et le transforme en objet connecté.

### Matériel

| Élément | Broche / interface |
|---|---|
| Carte | Arduino UNO R4 WiFi (RTC interne, module WiFi) |
| Capteur DHT22 | A0 |
| LCD Grove RGB 16x2 | I2C (SDA / SCL) |
| LED de vie | 2 |
| Bargraphe 10 LED | 3 → 12 |
| Port série | USB, 9600 bauds |

### Démarrage (`setup`)
1. Initialisation des broches, du LCD, du DHT22 et du RTC (date de départ fixée dans le code).
2. Connexion WiFi (10 s maximum), puis attente de l'adresse IP.
3. Synchronisation NTP (serveur `192.168.1.254`, décalage +2 h) et mise à jour du RTC.
4. Connexion au broker MQTT, puis abonnement aux topics `COMMAND`, `BARGRAPH` et `BLINK`.
5. Écran d'accueil n° 1 (3 s) : version + date, puis adresse IP (ou « Pas de wifi »).
6. Écran d'accueil n° 2 (3 s) : état MQTT (« Connecte » ou « Erreur <code> »).

### Ordonnancement (`loop`)
Le programme tourne dans une boucle de **100 ms** ; un compteur de tours cadence les tâches :

| Tâche | Période |
|---|---|
| Réception des messages MQTT (`mqttClient.poll()`) | 100 ms (chaque tour) |
| LED de vie (allumée la 1re moitié de la période) | 500 ms par défaut (2 Hz), modifiable |
| Affichage date et heure (ligne 1 du LCD) | 1 s |
| Mesure DHT22, envoi série, affichage ligne 2, publication MQTT | 2 s (si la mesure est active) |
| Resynchronisation NTP | 60 s |

Affichage :
- **Ligne 1** : date et heure du RTC (`J/M/AA HH:MM:SS`), ou « Pas de synchro » si la synchro NTP a échoué.
- **Ligne 2** : `T 21.3oC/H 45.0%` (même format sur le port série).

### MQTT

- Broker : `192.168.1.1`, port `1883`, avec authentification.
- Identifiant du capteur : `42914` (suffixe de tous les topics).

**Topics publiés**

| Topic | Contenu | Quand |
|---|---|---|
| `/iot/VERSION_42914` | Version au format `X.Y` (ex. `1.0`) | Après la commande 10, si la synchro NTP réussit |
| `/iot/TEMPERATURE_42914` | Température au dixième | Si la température ou l'humidité a changé (au dixième) |
| `/iot/HUMIDITY_42914` | Humidité au dixième | Idem |
| `/iot/GET_DATE_42914` | Date `JJ/MM/AAAA HH:MM:SS` | Idem |

**Topics souscrits**

| Topic | Valeur attendue | Effet |
|---|---|---|
| `/iot/COMMAND_42914` | Code de commande (voir ci-dessous) | Exécute la commande |
| `/iot/BARGRAPH_42914` | Entier 0 → 1023 | Allume 0 à 10 barres proportionnellement |
| `/iot/BLINK_42914` | Période en ms | Période personnalisée de la LED de vie (arrondie à 100 ms, minimum 200 ms) |

**Codes de commande**

| Code | Action |
|---|---|
| 10 | Force la synchro NTP, puis publie la version |
| 20 | Démarre la mesure |
| 30 | Arrête la mesure |
| 40 | Clignotement lent de la LED de vie (2000 ms) |
| 50 | Clignotement rapide (200 ms) |
| 60 | Clignotement avec la période reçue sur `BLINK` |

**Exemple de test** (avec les clients Mosquitto, depuis le même réseau) :

```bash
# écouter tout ce que publie le capteur
mosquitto_sub -h 192.168.1.1 -u <utilisateur> -P <mot_de_passe> -t "/iot/+_42914" -v

# demander la version, puis allumer la moitié du bargraphe
mosquitto_pub -h 192.168.1.1 -u <utilisateur> -P <mot_de_passe> -t "/iot/COMMAND_42914" -m 10
mosquitto_pub -h 192.168.1.1 -u <utilisateur> -P <mot_de_passe> -t "/iot/BARGRAPH_42914" -m 512
```

### Configuration
Le SSID, le mot de passe WiFi et les identifiants MQTT sont définis en tête de [TempHumiX.ino](TP_PRATIQUE/TempHumiX/TempHumiX.ino). Pour tester le WiFi 5 GHz, commenter la ligne du SSID 2,4 GHz et décommenter celle du SSID 5G.

## Prérequis

- Git
- Arduino IDE (1.8.19 ou 2.x) avec le paquet de cartes **Arduino UNO R4 Boards** (fournit `WiFiS3.h` et `RTC.h`)
- SimulIDE 1.1.0 (pour les exercices de simulation)
- Bibliothèques Arduino :
  - DHT sensor library (Adafruit) + Adafruit Unified Sensor
  - LiquidCrystal AIP31068 (`LiquidCrystal_AIP31068_I2C.h`) — exercices LCD simulés
  - Grove - LCD RGB Backlight (`rgb_lcd.h`) — TempHumiX
  - NTPClient
  - ArduinoMqttClient

## Utilisation

**Simulation (SimulIDE)**
1. Cloner le dépôt et se placer sur la branche `simulation`.
2. Ouvrir le circuit `.sim1` d'un exercice dans SimulIDE.
3. Ouvrir le `.ino` correspondant dans l'Arduino IDE et l'exporter en binaire compilé (`.hex`).
4. Dans SimulIDE : clic droit sur l'Arduino → *Charger firmware*, puis choisir le `.hex`.
5. Lancer la simulation.

**Carte réelle (UNO R4 WiFi)**
1. Se placer sur la branche `tp_pratique`.
2. Ouvrir `TP_PRATIQUE/TempHumiX/TempHumiX.ino` et adapter si besoin la configuration WiFi / MQTT en tête du fichier.
3. Sélectionner la carte *Arduino UNO R4 WiFi*, téléverser.
4. Ouvrir le moniteur série à 9600 bauds pour suivre la connexion et les mesures.

> Les fichiers compilés (`.hex`, `.elf`, `.bin`, `.o`) sont ignorés par Git.

## Historique du projet

1. Clignotement d'une LED
2. Bargraphe : chenillard 100 ms
3. Capteur DHT22 : LED verte / rouge selon la température
4. LCD I2C : « HELLO WORLD »
5. LCD I2C + DHT22 : affichage de l'école, de la température et de l'humidité
6. TempHumiX simulé : LED de vie, dateur, DHT22, LCD et port série
7. Ajout du RTC (UNO R4 WiFi)
8. Ajout du WiFi (test 2,4 GHz et 5 GHz)
9. Synchronisation NTP et mise à jour du RTC
10. Client MQTT : publication des mesures sur changement de valeur, commandes, bargraphe et LED de vie pilotables
