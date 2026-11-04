import sqlite3
from datetime import datetime
from paho.mqtt import client as mqtt_client


class ClientMQTT:
    def __init__(self, ip_address, port, client_id, username, password):
        super().__init__()
        self.ip_address = ip_address
        self.port = port
        self.client_id = client_id
        self.username = username
        self.password = password
        self.client = None
        self.version = "-"
        self.date_IdO = "-"
        self.temperature = None
        self.humidite = None
        self.id_capteur = None

        self.conn = None
        self.tablename = None

    # 3.2.1 - connexion au broker
    def connect_mqtt(self) -> mqtt_client:
        def on_connect(client, userdata, flags, rc, properties):
            if rc == 0:
                print(f"Connecté au broker MQTT : {self.ip_address} {self.port}")
            else:
                print(f"Echec de connexion au broker, code : {rc}")

        self.client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION2, client_id=self.client_id)
        self.client.username_pw_set(self.username, self.password)
        self.client.on_connect = on_connect
        self.client.connect(self.ip_address, self.port)
        return self.client

        # 3.2.2 - déconnexion
    def disconnect_mqtt(self) -> None:
        self.client.disconnect()
        print("Déconnecté du broker MQTT")

    # 3.2.3 - publication
    def publish_mqtt(self, topic, message, qos=0):
        self.client.publish(topic, message, qos)
        print(f"Publication : `{message}` sur `{topic}`")

    # 3.2.4 - souscription
    def subscribe_mqtt(self, topic, qos=0):
        def on_message(client, userdata, msg):
            valeur = msg.payload.decode()
            nom = msg.topic.upper()            # marche avec /iot/TEMPERATURE_ et /iot/temperature_
            self.id_capteur = int(msg.topic.split("_")[-1])
            if "VERSION_" in nom:
                self.version = valeur
            elif "GET_DATE_" in nom:
                self.date_IdO = valeur
            elif "TEMPERATURE_" in nom:
                self.temperature = float(valeur)
            elif "HUMIDITY_" in nom:
                self.humidite = float(valeur)
                self.save_sqlite()

        self.client.subscribe(topic, qos)
        self.client.on_message = on_message
        print(f"Attente du topic : `{topic}`")

    # attente des messages
    def wait_mqtt(self, timeout=0):
        if timeout == 0:
            self.client.loop_forever()
        else:
            self.client.loop(timeout=timeout)

    # ---------- SQLite---------
    def connect_sqlite(self, dbname="IOT.db", tablename="IOT_DATA"):
        self.conn = sqlite3.connect(dbname)
        self.tablename = tablename
        self.conn.cursor().execute(
            f"CREATE TABLE IF NOT EXISTS {tablename} "
            "(Id_capteur integer, Date text, Version text, Temperature real, Humidite real)")
        self.conn.commit()
        print(f"Base SQLite ouverte : {dbname} / table {tablename}")

    def disconnect_sqlite(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None
            print("Base SQLite fermée")

    def save_sqlite(self):
        if self.conn is None or self.temperature is None or self.date_IdO == "-":
            return
        # le capteur envoie JJ/MM/AAAA HH:MM:SS ; on stocke AAAA-MM-JJ HH:MM:SS pour pouvoir trier et filtrer
        date_iso = datetime.strptime(self.date_IdO, "%d/%m/%Y %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
        self.conn.cursor().execute(
            f"INSERT INTO {self.tablename} VALUES (?,?,?,?,?)",
            (self.id_capteur, date_iso, self.version, self.temperature, self.humidite))
        self.conn.commit()