# Projet IoT TempHumiX : capteur, MQTT et IHM

TempHumiX est un capteur IoT de température et d'humidité réalisé à l'IMT Nord Europe. Il repose sur une carte Arduino UNO R4 WiFi et un capteur DHT22.
Le capteur publie ses mesures en MQTT vers un broker Mosquitto et reçoit des commandes par le même chemin.
Une IHM Python (PySide6) se connecte au broker. Elle affiche les mesures, pilote le capteur, archive les données dans une base SQLite et trace les courbes entre deux dates.

## Sommaire

- [Les 3 parties du projet](#les-3-parties-du-projet)
- [Architecture](#architecture)
- [Topics MQTT et codes de commande](#topics-mqtt-et-codes-de-commande)
- [Installation de l'IHM (Windows)](#installation-de-lihm-windows)
- [Lancement](#lancement)
- [Notice d'utilisation de l'IHM](#notice-dutilisation-de-lihm)
- [Archivage SQLite](#archivage-sqlite)
- [Structure du dépôt](#structure-du-dépôt)
- [Choix techniques et écarts par rapport au sujet](#choix-techniques-et-écarts-par-rapport-au-sujet)
- [Dépannage](#dépannage)
- [Auteur](#auteur)

## Les 3 parties du projet

| Partie | Dossier | Branche Git | Contenu |
|---|---|---|---|
| 1. Simulation | [SIMULIDE/](SIMULIDE/) | `simulation` | Exercices SimulIDE sur Arduino Uno (LED, bargraphe, DHT22, LCD I2C) et un premier TempHumiX autonome. Chaque dossier contient un circuit `.sim1` et son programme `.ino`. |
| 2. Capteur réel | [TP_PRATIQUE/](TP_PRATIQUE/) | `tp_pratique` | TempHumiX sur UNO R4 WiFi : RTC, WiFi, synchronisation NTP, client MQTT pilotable à distance. |
| 3. IHM Python | [IHM/](IHM/) | `ihm` | Consoles MQTT, capteur simulé, IHM PySide6 avec archivage SQLite et courbes Matplotlib. |

La branche `main` regroupe les parties 1, 2 et 3 (fusion de `tp_pratique` et `ihm`).


## Architecture

```text
  Capteur TempHumiX                      Broker MQTT                     IHM PySide6
  (UNO R4 WiFi + DHT22)                  port 1883                       (ihm_mqtt_simple)
  ou capteur_simule.py                   Mosquitto (école)
                                         amqtt (maison)
 +---------------------+               +----------------+              +----------------------+
 |                     | --publie----> |                | --transmet-> |                      |
 |                     |  VERSION_     |                |              | thread MQTT          |
 |                     |  GET_DATE_    |                |              |   -> SQLite IOT.db   |
 |                     |  TEMPERATURE_ |                |              | QTimer 1 s           |
 |                     |  HUMIDITY_    |                |              |   -> affichage       |
 |                     |               |                |              |                      |
 |                     | <--transmet-- |                | <---publie-- | boutons / champs     |
 |                     |  COMMAND_     |                |  COMMAND_    |                      |
 |                     |  BARGRAPH_    |                |  BARGRAPH_   |                      |
 |                     |  BLINK_       |                |  BLINK_      |                      |
 +---------------------+               +----------------+              +----------------------+

 Tous les topics ont la forme /iot/<NOM>_42914
```

## Topics MQTT et codes de commande

Format des topics : `/iot/<NOM>_42914`, où `42914` est l'identifiant du poste. Les noms sont en majuscules.

| Topic | Sens | Contenu | Format |
|---|---|---|---|
| `/iot/VERSION_42914` | capteur → IHM | Version du programme du capteur | `X.Y`, par exemple `1.0` |
| `/iot/GET_DATE_42914` | capteur → IHM | Date et heure de la mesure | `JJ/MM/AAAA HH:MM:SS` |
| `/iot/TEMPERATURE_42914` | capteur → IHM | Température en °C | réel au dixième, par exemple `21.3` |
| `/iot/HUMIDITY_42914` | capteur → IHM | Humidité relative en % | réel au dixième, par exemple `45.0` |
| `/iot/COMMAND_42914` | IHM → capteur | Code de commande | entier `10` à `60` (voir ci-dessous) |
| `/iot/BARGRAPH_42914` | IHM → capteur | Valeur du bargraphe | entier `0` à `1023`, allume 0 à 10 barres |
| `/iot/BLINK_42914` | IHM → capteur | Période personnalisée de la LED de vie | entier en ms, arrondi à 100 ms, minimum 200 ms |
| `/iot/DATA_42914` | capteur → IHM | Option `--data` du capteur simulé uniquement, non lu par l'IHM | `JJ/MM/AAAA HH:MM:SS\|T\|H` |

Les mesures sont publiées toutes les 2 s, seulement si la température ou l'humidité a changé. La version n'est publiée qu'après la commande 10 (et, pour le capteur simulé, aussi à sa connexion).

| Code | Action sur le capteur |
|---|---|
| 10 | Synchronisation NTP puis publication de la version (sur le capteur réel, seulement si la synchro réussit) |
| 20 | Démarre la mesure |
| 30 | Arrête la mesure |
| 40 | LED de vie en clignotement lent (2000 ms) |
| 50 | LED de vie en clignotement rapide (200 ms) |
| 60 | LED de vie avec la période reçue sur `BLINK_` |

## Installation de l'IHM (Windows)

L'IHM utilise [uv](https://docs.astral.sh/uv/) pour gérer Python et les dépendances. Python 3.12 est requis (`requires-python = ">=3.12,<3.13"` dans [pyproject.toml](IHM/pyproject.toml)).

1. Installer uv :

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Fermer puis rouvrir le terminal pour que la commande `uv` soit reconnue.

2. Récupérer le dépôt sur la branche `ihm` :

```powershell
git clone https://github.com/jam-bri/IOT_BY.git
cd IOT_BY
git checkout ihm
```

3. Installer Python 3.12 et les dépendances :

```powershell
cd IHM
uv python install 3.12
uv sync
```

`uv sync` crée le dossier `IHM\.venv` et installe les versions figées dans `uv.lock` : paho-mqtt, PySide6, matplotlib, et amqtt (groupe `dev`, pour le broker local).

Le dossier `.venv` n'est pas versionné (il est dans `.gitignore`). Chaque poste le recrée avec `uv sync`.

## Lancement

Ouvrir trois terminaux PowerShell, dans cet ordre.

**Terminal 1 : broker local** (à la maison uniquement)

```powershell
cd IOT_BY\IHM
uv run amqtt -c broker.yaml
```

Le broker écoute sur `127.0.0.1:1883` et accepte les connexions anonymes. Laisser ce terminal ouvert.

**Terminal 2 : IHM**

```powershell
cd IOT_BY\IHM\ihm_mqtt_simple
uv run python main.py
```

Lancer l'IHM depuis `ihm_mqtt_simple` : la base `IOT.db` est créée dans le dossier courant. Cliquer sur **Connecter** avant de lancer le capteur.

**Terminal 3 : capteur simulé**

```powershell
cd IOT_BY\IHM
uv run python capteur_simule.py
```

`capteur_simule.py` remplace le boîtier réel car on n'a pas accès à la salle de TP. Il publie les mêmes topics que l'Arduino et réagit aux mêmes commandes (affichage dans la console). Options :

| Option | Effet |
|---|---|
| `--id 42914` | Identifiant du capteur (suffixe des topics). Par défaut 42914. |
| `--nb 3` | Simule plusieurs capteurs : 42914, 42915, 42916. |
| `--data` | Publie aussi le topic sérialisé `DATA_`. |
| `--minuscules` | Topics en minuscules (`/iot/temperature_42914`). L'IHM ne les reçoit plus. |
| `--broker 10.120.2.3` | Adresse du broker. Par défaut 127.0.0.1. |

Seule l'adresse du broker change entre la maison et l'école :

| Lieu | Broker | Champ « Broker » de l'IHM |
|---|---|---|
| Local | amqtt local (terminal 1) | `127.0.0.1` |
| École | Mosquitto de la salle de TP, pas de terminal 1 | `10.120.2.3` |

Le port reste `1883`. Identifiants : `mos_user` / `mos_user`.

Note : le programme Arduino se connecte au broker `192.168.1.1` (constante `IP_HOST`). [À vérifier : correspondance entre 192.168.1.1 côté capteur et 10.120.2.3 côté PC.]

## Notice d'utilisation de l'IHM


### Zone « Connexion au broker »

| Élément | Rôle |
|---|---|
| Broker | Adresse du broker. Par défaut `127.0.0.1`. |
| Port | Par défaut `1883`. |
| Id capteur | Par défaut `42914`. Sert à construire les topics. |
| Connecter | Se connecte au broker, lance le thread MQTT (abonnement aux 4 topics du capteur, ouverture de `IOT.db`) et démarre l'affichage toutes les secondes. |
| Déconnecter | Arrête l'affichage, arrête le thread (au plus 1 s), ferme la base et se déconnecte. |

La barre d'état indique l'état de la connexion, l'adresse du broker et le capteur suivi. Si le broker ne répond pas, elle affiche « Broker injoignable ». Le menu **Fichier > Quitter** ferme proprement la fenêtre.

### Zone « Données du capteur »

Affiche la version, la date et l'heure, la température (°C) et l'humidité (%). Les valeurs sont rafraîchies toutes les secondes. Tant que rien n'est reçu, elles restent à « - ».

### Zone « Commandes »

Cette zone n'est active qu'une fois connecté.

| Bouton ou champ | Topic | Valeur envoyée |
|---|---|---|
| Mise à l'heure | `COMMAND_` | `10` |
| Démarrer mesure | `COMMAND_` | `20` puis `50` (clignotement rapide pendant la mesure) |
| Arrêter mesure | `COMMAND_` | `30` puis `40` (clignotement lent à l'arrêt) |
| Clignotement lent | `COMMAND_` | `40` |
| Clignotement rapide | `COMMAND_` | `50` |
| Période (ms) + Clignotement perso | `BLINK_` puis `COMMAND_` | la période saisie, puis `60` |
| Bargraphe (0-1023) | `BARGRAPH_` | la valeur saisie, envoyée à l'appui sur **Entrée** |
| Courbes... | aucun | ouvre la fenêtre des courbes |

Le champ **Période** accepte un nombre de 3 à 5 chiffres (1000 par défaut). Le capteur l'arrondit à 100 ms, avec un minimum de 200 ms. Le champ **Bargraphe** n'accepte que les entiers de 0 à 1023.

### Fenêtre des courbes


- **Début** et **Fin** : période à afficher, au format `AAAA-MM-JJ HH:MM:SS`. Par défaut, la dernière heure.
- **Charger les données** : lit `IOT.db` pour le capteur courant et trace la température et l'humidité en fonction de l'heure. Le titre indique le nombre de mesures. S'il n'y a rien, la fenêtre affiche « Aucune donnée sur cette période ».
- **Effacer les courbes** : vide le graphique.

## Archivage SQLite

- Fichier : `IOT.db`, créé dans le dossier de lancement (`IHM\ihm_mqtt_simple`). Il n'est pas versionné (`*.db` dans `.gitignore`).
- Table : `IOT_DATA`, créée si elle n'existe pas.

| Colonne | Type | Contenu |
|---|---|---|
| `Id_capteur` | integer | Identifiant lu à la fin du topic (42914) |
| `Date` | text | Date de la mesure, `AAAA-MM-JJ HH:MM:SS` |
| `Version` | text | Dernière version reçue (« - » si aucune) |
| `Temperature` | real | Dernière température reçue |
| `Humidite` | real | Humidité reçue |

Une ligne est enregistrée à chaque réception de `HUMIDITY_`. L'humidité sert de déclencheur car c'est le dernier topic publié par le capteur simulé (ordre : date, température, humidité). L'enregistrement est ignoré tant qu'aucune date ni température n'a été reçue.

Le capteur envoie la date au format `JJ/MM/AAAA HH:MM:SS`. L'IHM la convertit en `AAAA-MM-JJ HH:MM:SS` avant de l'enregistrer. SQLite stocke ici la date comme du texte. Dans ce format, l'ordre alphabétique est aussi l'ordre chronologique. `ORDER BY Date` et `Date BETWEEN début AND fin` fonctionnent donc directement. C'est aussi le format des champs Début et Fin de la fenêtre des courbes.

## Structure du dépôt

```text
IOT_BY/
├── .gitignore                       # exclut .venv, __pycache__, *.db, fichiers compilés Arduino
├── README.md                        # ce fichier
├── SIMULIDE/                        # partie 1 : simulation SimulIDE (Arduino Uno)
│   ├── clignotement_led/            # LED qui clignote
│   ├── bargraphe/                   # chenillard sur 10 LED
│   ├── capteur_dht22/               # LED verte / rouge selon la température
│   ├── lcd_i2c/                     # « HELLO WORLD » sur LCD I2C
│   ├── lcd_i2c_dht22/               # LCD + DHT22 : école, température, humidité
│   └── TempHumiX/                   # TempHumiX simulé (.ino + circuit .sim1)
├── TP_PRATIQUE/                     # partie 2 : carte réelle UNO R4 WiFi
│   └── TempHumiX/TempHumiX.ino      # RTC, WiFi, NTP, client MQTT
└── IHM/                             # partie 3 : IHM Python
    ├── pyproject.toml               # projet uv : Python 3.12, dépendances
    ├── uv.lock                      # versions figées des dépendances
    ├── broker.yaml                  # configuration du broker local amqtt (127.0.0.1:1883)
    ├── capteur_simule.py            # capteur simulé, remplace le boîtier réel
    ├── console_mqtt_lecture/        # étape 1 : console qui affiche les topics reçus
    │   ├── client_mqtt.py           # classe ClientMQTT (connexion, publication, souscription)
    │   └── main.py
    ├── console_mqtt_ecriture/       # étape 2 : console menu qui envoie les commandes
    │   ├── client_mqtt.py
    │   └── main.py
    ├── console_mqtt_thread/         # étape 3 : lecture dans un thread + menu
    │   ├── client_mqtt.py
    │   ├── thread_mqtt.py           # classe ThreadMQTT
    │   └── main.py
    └── ihm_mqtt_simple/             # étape 4 : IHM graphique finale
        ├── main.py                  # fenêtre principale, boutons, QTimer d'affichage
        ├── client_mqtt.py           # ClientMQTT + mémorisation des valeurs + archivage SQLite
        ├── thread_mqtt.py           # thread de réception MQTT, ouvre et ferme la base
        ├── dialogue_courbe.py       # fenêtre des courbes (requête SQLite + Matplotlib)
        ├── mon_ihm.ui               # fenêtre principale dessinée dans Qt Designer
        ├── mon_ihm.py               # code généré depuis mon_ihm.ui
        ├── graphe.ui                # fenêtre des courbes dessinée dans Qt Designer
        └── graphe.py                # code généré depuis graphe.ui
```



## Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Barre d'état : « Broker injoignable : ... » au clic sur Connecter | Le broker n'est pas lancé, ou l'adresse est fausse | À la maison, lancer `uv run amqtt -c broker.yaml` dans `IHM`. À l'école, saisir `10.120.2.3`. |
| Connecté, mais rien ne s'affiche | Topics différents : capteur lancé avec `--minuscules`, ou Id capteur différent entre IHM et capteur | Relancer le capteur sans `--minuscules`. Mettre le même identifiant dans le champ Id capteur et dans `--id`. |
| Rien ne s'affiche, la mesure semble arrêtée | La commande 30 a été envoyée | Cliquer sur **Démarrer mesure**. |
| Déconnexions répétées, barre d'état « Connexion en cours / perdue » | Identifiant client en double : deux clients `Client_42914` (IHM + console de lecture ou console thread), ou `IdO_Client_42914` (boîtier réel + capteur simulé). Le broker coupe l'ancien client. | Ne lancer qu'une IHM ou console à la fois. Ne pas lancer le capteur simulé quand le boîtier réel est branché sur le même broker. |
| `ModuleNotFoundError: No module named 'PySide6'` (ou `paho`, `matplotlib`) | Script lancé avec le Python du système au lieu de l'environnement uv, ou `uv sync` non fait | Faire `uv sync` dans `IHM`, puis lancer avec `uv run python main.py`. |
| `ModuleNotFoundError: No module named 'mon_ihm'` (ou `client_mqtt`) | Fichier généré absent, ou mauvais script lancé | Vérifier que `mon_ihm.py` et `graphe.py` existent (sinon les régénérer, voir plus haut). Lancer `main.py` depuis `IHM\ihm_mqtt_simple`. |
| La version reste à « - » | La version n'est publiée qu'après la commande 10, et elle n'est pas conservée par le broker. Si l'IHM se connecte après le capteur simulé, elle a manqué sa publication. Sur le boîtier réel, la version n'est publiée que si la synchro NTP réussit. | Cliquer sur **Mise à l'heure**. Sur le boîtier réel, vérifier la synchro NTP (moniteur série, 9600 bauds). |
| Courbes : « Aucune donnée sur cette période » | Pas de mesures archivées sur la période, ou IHM lancée depuis un autre dossier (autre `IOT.db`) | Élargir Début / Fin. Toujours lancer l'IHM depuis `IHM\ihm_mqtt_simple`. |

## Auteur

- Auteur : Briana Y
- Dépôt : IOT_BY ([github.com/jam-bri/IOT_BY](https://github.com/jam-bri/IOT_BY))
- Poste : 42914
- École : IMT Nord Europe, FISE2027 - SISC
