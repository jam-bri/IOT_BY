from threading import Thread


class ThreadMQTT(Thread):
    def __init__(self, client_mqtt, id_pc):
        Thread.__init__(self)
        self.mqtt = client_mqtt
        self.id_pc = id_pc
        self.stop = False

    def run(self):
        for nom in ("VERSION", "GET_DATE", "TEMPERATURE", "HUMIDITY"):
            self.mqtt.subscribe_mqtt(f"/iot/{nom}_{self.id_pc}")
        while not self.stop:
            self.mqtt.wait_mqtt(timeout=1.0)     # traite les messages, rend la main au plus tard après 1 s

    def stopthread(self):
        self.stop = True