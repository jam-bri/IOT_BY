from client_mqtt import ClientMQTT

id_pc = 42914
broker = "127.0.0.1"      # en local car par reseau ecole 
port = 1883
username = "mos_user"
password = "mos_user"

# mêmes noms que votre Arduino (majuscules)
topic_version = f"/iot/VERSION_{id_pc}"
topic_temperature = f"/iot/TEMPERATURE_{id_pc}"
topic_humidite = f"/iot/HUMIDITY_{id_pc}"
topic_date = f"/iot/GET_DATE_{id_pc}"

if __name__ == '__main__':
    print("Démarrage de l'application")
    print("==========================")
    print("Instanciation de votre ClientMQTT")
    mqtt = ClientMQTT(broker, port, f"Client_{id_pc}", username, password)
    mqtt.connect_mqtt()

    print(f"Souscription aux données du capteur : 'Client_{id_pc}'")
    mqtt.subscribe_mqtt(topic_version)
    mqtt.subscribe_mqtt(topic_temperature)
    mqtt.subscribe_mqtt(topic_humidite)
    mqtt.subscribe_mqtt(topic_date)

    # Attente des valeurs souscrites avec timeout=0 (Ctrl+C pour arrêter)
    try:
        mqtt.wait_mqtt(timeout=0)
    except KeyboardInterrupt:
        mqtt.disconnect_mqtt()

    print("Fin de l'application")