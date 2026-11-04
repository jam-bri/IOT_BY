"""
Capteur IdO simulé – remplace le boîtier Arduino TempHumiX pour travailler à la maison.

Il fait la même chose que le programme Arduino :
  - publie VERSION_, GET_DATE_, TEMPERATURE_, HUMIDITY_ toutes les 2 s (seulement si T ou H change)
  - écoute COMMAND_, BARGRAPH_, BLINK_ et réagit (affichage dans la console)

Lancement :   python capteur_simule.py
Options   :   python capteur_simule.py --broker 127.0.0.1 --id 42914
              python capteur_simule.py --nb 3          (3 capteurs : 42914, 42915, 42916)
              python capteur_simule.py --data          (ajoute le topic sérialisé DATA_ du challenge)
"""
import argparse
import random
import threading
import time
from datetime import datetime

from paho.mqtt import client as mqtt_client

# ---------- paramètres par défaut (à adapter) ----------
BROKER = "127.0.0.1"      # chez vous : broker local. En TP : 10.120.2.3
PORT = 1883
USERNAME = "mos_user"
PASSWORD = "mos_user"
ID_PC = 42914
GROUPE = "/iot/"
MAJUSCULES = True         # True = comme votre Arduino (/iot/TEMPERATURE_42914)
VERSION = "1.0"

PERIODE_NORMALE = 500
PERIODE_LENTE = 2000
PERIODE_RAPIDE = 200


class CapteurSimule:
    def __init__(self, id_capteur, broker, port, username, password, majuscules, data, temp0, hum0):
        self.id = id_capteur
        self.majuscules = majuscules
        self.data = data
        self.mesure_active = True
        self.periode_vie = PERIODE_NORMALE
        self.periode_perso = 1000
        self.bargraph = 0
        self.temp = temp0
        self.hum = hum0
        self.derniere_publiee = None
        self.stop = False

        self.client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION2,
                                         client_id=f"IdO_Client_{id_capteur}")
        self.client.username_pw_set(username, password)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(broker, port)

    # nom d'un topic, en majuscules ou minuscules selon le réglage
    def topic(self, nom):
        nom = nom if self.majuscules else nom.lower()
        return f"{GROUPE}{nom}_{self.id}"

    def log(self, texte):
        print(f"[{datetime.now():%H:%M:%S}] capteur {self.id} | {texte}")

    def on_connect(self, client, userdata, flags, rc, properties):
        if rc == 0:
            self.log("connecté au broker")
            for nom in ("COMMAND", "BARGRAPH", "BLINK"):
                client.subscribe(self.topic(nom))
            self.publier_version()
        else:
            self.log(f"échec de connexion, code {rc}")

    def on_message(self, client, userdata, msg):
        texte = msg.payload.decode(errors="replace").strip()
        try:
            valeur = int(float(texte))
        except ValueError:
            self.log(f"message ignoré sur {msg.topic} : '{texte}' (pas un nombre)")
            return
        nom = msg.topic.upper()
        if "COMMAND" in nom:
            self.traiter_commande(valeur)
        elif "BARGRAPH" in nom:
            self.bargraph = max(0, min(1023, valeur))
            nb = round(self.bargraph * 10 / 1023)
            self.log(f"bargraphe = {self.bargraph:4d}  [{'█' * nb}{'░' * (10 - nb)}]")
        elif "BLINK" in nom:
            self.periode_perso = max(200, (valeur // 100) * 100)
            self.log(f"période perso enregistrée : {self.periode_perso} ms")

    def traiter_commande(self, code):
        if code == 10:
            self.log("commande 10 : synchro NTP -> publication de la version")
            self.publier_version()
        elif code == 20:
            self.mesure_active = True
            self.log("commande 20 : mesures DÉMARRÉES")
        elif code == 30:
            self.mesure_active = False
            self.log("commande 30 : mesures ARRÊTÉES")
        elif code == 40:
            self.periode_vie = PERIODE_LENTE
            self.log("commande 40 : LED de vie LENTE (2000 ms)")
        elif code == 50:
            self.periode_vie = PERIODE_RAPIDE
            self.log("commande 50 : LED de vie RAPIDE (200 ms)")
        elif code == 60:
            self.periode_vie = self.periode_perso
            self.log(f"commande 60 : LED de vie PERSO ({self.periode_perso} ms)")
        else:
            self.log(f"code commande inconnu : {code}")

    def publier_version(self):
        self.client.publish(self.topic("VERSION"), VERSION)

    def mesurer(self):
        # petite marche aléatoire, arrondie au dixième comme le DHT22
        self.temp = round(min(35, max(15, self.temp + random.choice([-0.1, 0, 0, 0.1, 0.2, -0.2]))), 1)
        self.hum = round(min(80, max(25, self.hum + random.choice([-0.3, -0.1, 0, 0.1, 0.3]))), 1)

    def publier_mesures(self):
        date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # même ordre que le TP : HUMIDITY en dernier (c'est lui qui déclenche l'archivage)
        self.client.publish(self.topic("GET_DATE"), date)
        self.client.publish(self.topic("TEMPERATURE"), f"{self.temp:.1f}")
        self.client.publish(self.topic("HUMIDITY"), f"{self.hum:.1f}")
        if self.data:
            self.client.publish(self.topic("DATA"), f"{date}|{self.temp:.3f}|{self.hum:.3f}", qos=1, retain=True)
        self.log(f"{date}  T {self.temp:.1f} °C  H {self.hum:.1f} %")

    def run(self):
        self.client.loop_start()
        compteur = 0
        while not self.stop:
            time.sleep(0.1)
            compteur += 1
            if compteur % 20 == 0 and self.mesure_active:      # toutes les 2 s
                self.mesurer()
                valeurs = (self.temp, self.hum)
                if valeurs != self.derniere_publiee:
                    self.publier_mesures()
                    self.derniere_publiee = valeurs
        self.client.loop_stop()
        self.client.disconnect()


def main():
    p = argparse.ArgumentParser(description="Capteur IdO simulé (TempHumiX)")
    p.add_argument("--broker", default=BROKER)
    p.add_argument("--port", type=int, default=PORT)
    p.add_argument("--user", default=USERNAME)
    p.add_argument("--password", default=PASSWORD)
    p.add_argument("--id", type=int, default=ID_PC, help="numéro du PC (44xxx / 42xxx)")
    p.add_argument("--nb", type=int, default=1, help="nombre de capteurs simulés (challenge)")
    p.add_argument("--minuscules", action="store_true", help="topics en minuscules (/iot/temperature_xxxxx)")
    p.add_argument("--data", action="store_true", help="publie aussi le topic sérialisé DATA_ (challenge)")
    a = p.parse_args()

    capteurs = []
    for i in range(a.nb):
        c = CapteurSimule(a.id + i, a.broker, a.port, a.user, a.password,
                          not a.minuscules, a.data, 22.0 + 1.5 * i, 50.0 - 4 * i)
        capteurs.append(c)
        threading.Thread(target=c.run, daemon=True).start()

    print("Capteur(s) simulé(s) lancé(s). Ctrl+C pour arrêter.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        for c in capteurs:
            c.stop = True
        time.sleep(0.5)
        print("Arrêt du capteur simulé.")


if __name__ == "__main__":
    main()
