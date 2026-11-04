import time

from client_mqtt import ClientMQTT

id_pc = 42914
broker = "127.0.0.1"      # local ; dans le reseau école : "10.120.2.3"
port = 1883
username = "mos_user"
password = "mos_user"

topic_commande = f"/iot/COMMAND_{id_pc}"
topic_bargraphe = f"/iot/BARGRAPH_{id_pc}"
topic_periode = f"/iot/BLINK_{id_pc}"

if __name__ == '__main__':
    print("Démarrage de l'application")
    print("==========================")
    print("Instanciation de votre ClientMQTT")
    # 'E' dans l'identifiant : 2 clients connectés en même temps ne peuvent pas avoir le même Id 
    mqtt = ClientMQTT(broker, port, f"Client_E{id_pc}", username, password)
    mqtt.connect_mqtt()
    mqtt.client.loop_start()      # le réseau tourne en arrière-plan pendant que input() attend
    # attendre la réponse du broker avant d'afficher le menu (5 s maximum)
    for _ in range(50):
        if mqtt.client.is_connected():
            break
        time.sleep(0.1)
    if not mqtt.client.is_connected():
        print("Broker injoignable : vérifiez qu'il est lancé")

    car = ' '
    while car.upper() != 'Q':
        print()
        print("Console capteur IdO")
        print("-------------------")
        print("1 - Mise à l'heure du capteur")
        print("2 - Démarrage des mesures")
        print("3 - Arrêt des mesures")
        print("4 - Clignotement lent")
        print("5 - Clignotement rapide")
        print("6 - Clignotement personnalisé")
        print("7 - Ecriture du bargraphe")
        print("Q - Quitter")
        car = input("Votre choix : ")
        match car.upper():
            case '1':
                mqtt.publish_mqtt(topic_commande, "10")
                print(f"Synchronisation du capteur : {id_pc}")
            case '2':
                mqtt.publish_mqtt(topic_commande, "20")
                print(f"Démarrage des mesures sur le capteur : {id_pc}")
                mqtt.publish_mqtt(topic_commande, "50")      # mesure démarrée => clignotement rapide
            case '3':
                mqtt.publish_mqtt(topic_commande, "30")
                print(f"Arrêt des mesures sur le capteur : {id_pc}")
                mqtt.publish_mqtt(topic_commande, "40")      # mesure arrêtée => clignotement lent
            case '4':
                mqtt.publish_mqtt(topic_commande, "40")
                print(f"Clignotement lent de la led de vie du capteur : {id_pc}")
            case '5':
                mqtt.publish_mqtt(topic_commande, "50")
                print(f"Clignotement rapide de la led de vie du capteur : {id_pc}")
            case '6':
                periode = input("Période de clignotement en ms (multiple de 100) : ")
                if periode.isdigit():
                    mqtt.publish_mqtt(topic_periode, periode)
                    mqtt.publish_mqtt(topic_commande, "60")
                    print(f"Clignotement personnalisé ({periode} ms) du capteur : {id_pc}")
                else:
                    print("Valeur invalide")
            case '7':
                valeur = input("Choisir la valeur à écrire sur le bargraphe (0 à 1023) : ")
                if valeur.isdigit() and 0 <= int(valeur) <= 1023:
                    mqtt.publish_mqtt(topic_bargraphe, valeur)
                    print(f"Ecriture de la valeur {valeur} sur le bargraphe du capteur : {id_pc}")
                else:
                    print("Valeur invalide (0 à 1023)")
            case 'Q':
                print("Arrêt du client MQTT")
            case _:
                print("Choix inconnu")

    time.sleep(0.5)               # laisse partir les derniers messages avant de couper
    mqtt.client.loop_stop()
    mqtt.disconnect_mqtt()
    print("Fin de l'application")