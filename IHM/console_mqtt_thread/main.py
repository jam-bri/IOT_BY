import time

from client_mqtt import ClientMQTT
from thread_mqtt import ThreadMQTT

id_pc = 42914
broker = "127.0.0.1"      # local ; à l'école : "10.120.2.3"
port = 1883
username = "mos_user"
password = "mos_user"

topic_commande = f"/iot/COMMAND_{id_pc}"
topic_bargraphe = f"/iot/BARGRAPH_{id_pc}"

if __name__ == '__main__':
    print("Démarrage de l'application")
    print("==========================")
    mqtt = ClientMQTT(broker, port, f"Client_{id_pc}", username, password)
    mqtt.connect_mqtt()

    # a) créer le thread de lecture  et le lancer
    thread_mqtt = ThreadMQTT(mqtt, id_pc)
    thread_mqtt.start()

    # attendre la réponse du broker, traitée par le thread, avant d'afficher le menu
    for _ in range(50):
        if mqtt.client.is_connected():
            break
        time.sleep(0.1)

    car = ' '
    while car.upper() != 'Q':
        print()
        print("Console capteur IdO (avec thread)")
        print("---------------------------------")
        print("A - Afficher les dernières valeurs")
        print("2 - Démarrage des mesures")
        print("3 - Arrêt des mesures")
        print("7 - Ecriture du bargraphe")
        print("Q - Quitter")
        car = input("Votre choix : ")
        match car.upper():
            case 'A':
                print(f"Version : {mqtt.version}")
                print(f"Date    : {mqtt.date_IdO}")
                print(f"Temp.   : {mqtt.temperature} °C")
                print(f"Humid.  : {mqtt.humidite} %")
            case '2':
                mqtt.publish_mqtt(topic_commande, "20")
                mqtt.publish_mqtt(topic_commande, "50")
            case '3':
                mqtt.publish_mqtt(topic_commande, "30")
                mqtt.publish_mqtt(topic_commande, "40")
            case '7':
                valeur = input("Valeur du bargraphe (0 à 1023) : ")
                if valeur.isdigit() and 0 <= int(valeur) <= 1023:
                    mqtt.publish_mqtt(topic_bargraphe, valeur)
                else:
                    print("Valeur invalide (0 à 1023)")
            case 'Q':
                print("Arrêt du client MQTT")
            case _:
                print("Choix inconnu")

    # arrêt propre : lever le drapeau, attendre la fin du thread, puis se déconnecter
    thread_mqtt.stopthread()
    thread_mqtt.join()
    mqtt.disconnect_mqtt()
    print("Fin de l'application")