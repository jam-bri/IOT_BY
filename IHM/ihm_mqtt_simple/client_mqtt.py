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
            if "VERSION_" in nom:
                self.version = valeur
            elif "GET_DATE_" in nom:
                self.date_IdO = valeur
            elif "TEMPERATURE_" in nom:
                self.temperature = float(valeur)
            elif "HUMIDITY_" in nom:
                self.humidite = float(valeur)

        self.client.subscribe(topic, qos)
        self.client.on_message = on_message
        print(f"Attente du topic : `{topic}`")

    # 3.2.5 - attente des messages
    def wait_mqtt(self, timeout=0):
        if timeout == 0:
            self.client.loop_forever()
        else:
            self.client.loop(timeout=timeout)