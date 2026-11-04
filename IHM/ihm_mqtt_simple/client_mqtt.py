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
            print(f"Réception : `{msg.payload.decode()}` depuis '{msg.topic}'")

        self.client.subscribe(topic, qos)
        self.client.on_message = on_message
        print(f"Attente du topic : `{topic}`")

    # 3.2.5 - attente des messages
    def wait_mqtt(self, timeout=0):
        if timeout == 0:
            self.client.loop_forever()
        else:
            self.client.loop(timeout=timeout)