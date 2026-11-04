import sys

from PySide6.QtCore import QTimer, QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import QApplication, QMainWindow

from client_mqtt import ClientMQTT
from thread_mqtt import ThreadMQTT
from mon_ihm import Ui_MainWindow

from dialogue_courbe import CourbeDialog

username = 'mos_user'
password = 'mos_user'


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)          # construit tous les widgets dessinés dans Qt Designer

        self.mqtt = None
        self.thread_mqtt = None
        self.id_pc = None

        # timer d'affichage : appelle display() toutes les secondes une fois démarré
        self.timer = QTimer()
        self.timer.timeout.connect(self.display)

        # signal (clic) -> slot (méthode appelée)
        self.btnConnect.clicked.connect(self.connectMQTT)
        self.btnGraph.clicked.connect(self.showGraph)
        self.btnDisconnect.clicked.connect(self.disconnectMQTT)
        self.actionQuit.triggered.connect(self.close)
        self.btnSynchroDateTime.clicked.connect(self.synchroDateTime)
        self.btnStartMeasure.clicked.connect(self.startMeasure)
        self.btnStopMeasure.clicked.connect(self.stopMeasure)
        self.btnFastBlink.clicked.connect(self.fastBlink)
        self.btnSlowBlink.clicked.connect(self.slowBlink)
        self.btnBlink.clicked.connect(self.customBlink)
        self.lneBargraph.returnPressed.connect(self.setBargraph)

        # saisie contrôlée : 0 à 1023 pour le bargraphe, nombre pour la période
        self.lneBargraph.setValidator(QRegularExpressionValidator(
            QRegularExpression(r"^(\d{1,3}|10[01]\d|102[0-3])$")))
        self.lnePeriod.setValidator(QRegularExpressionValidator(QRegularExpression(r"^\d{3,5}$")))

        self.etat_boutons(connecte=False)
        self.statusbar.showMessage("Non connecté")

    # active / désactive les boutons selon l'état de la connexion
    def etat_boutons(self, connecte):
        self.btnConnect.setEnabled(not connecte)
        self.btnDisconnect.setEnabled(connecte)
        self.grpCommandes.setEnabled(connecte)

    # ---------- affichage ----------
    def display(self):
        m = self.mqtt
        self.lblVersion.setText(m.version)
        self.lblDate.setText(m.date_IdO)
        self.lblTemperature.setText("- °C" if m.temperature is None else f"{m.temperature:.1f} °C")
        self.lblHumidity.setText("- %" if m.humidite is None else f"{m.humidite:.1f} %")
        etat = "Connecté" if m.client.is_connected() else "Connexion en cours / perdue"
        self.statusbar.showMessage(f"{etat} à {m.ip_address}:{m.port} - capteur {self.id_pc}")

    # ---------- connexion ----------
    def connectMQTT(self):
        broker = self.lneBroker.text()
        port = int(self.lnePort.text())
        self.id_pc = int(self.lneIdCapteur.text())
        try:
            self.mqtt = ClientMQTT(broker, port, f"Client_{self.id_pc}", username, password)
            self.mqtt.connect_mqtt()
        except OSError as e:
            self.statusbar.showMessage(f"Broker injoignable : {e}")
            return
        self.thread_mqtt = ThreadMQTT(self.mqtt, self.id_pc)
        self.thread_mqtt.start()
        self.timer.start(1000)
        self.etat_boutons(connecte=True)

    def disconnectMQTT(self):
        self.timer.stop()
        if self.thread_mqtt is not None:
            self.thread_mqtt.stopthread()
            self.thread_mqtt.join()          # attend la fin propre du thread (au plus 1 s)
            self.thread_mqtt = None
        if self.mqtt is not None:
            self.mqtt.disconnect_mqtt()
        self.etat_boutons(connecte=False)
        self.statusbar.showMessage("Déconnecté")

    # ---------- commandes ----------
    def commande(self, code):
        self.mqtt.publish_mqtt(f"/iot/COMMAND_{self.id_pc}", str(code))

    def synchroDateTime(self):
        self.commande(10)

    def startMeasure(self):
        self.commande(20)
        self.commande(50)        # mesure démarrée => clignotement rapide

    def stopMeasure(self):
        self.commande(30)
        self.commande(40)        # mesure arrêtée => clignotement lent

    def fastBlink(self):
        self.commande(50)

    def slowBlink(self):
        self.commande(40)

    def customBlink(self):
        periode = self.lnePeriod.text()
        if periode:
            self.mqtt.publish_mqtt(f"/iot/BLINK_{self.id_pc}", periode)
            self.commande(60)

    def setBargraph(self):
        valeur = self.lneBargraph.text()
        if valeur:
            self.mqtt.publish_mqtt(f"/iot/BARGRAPH_{self.id_pc}", valeur)

    # ---------- courbes ----------
    def showGraph(self):
        dialogue = CourbeDialog(self.id_pc or 42914)
        dialogue.exec()

    # appelé à la fermeture de la fenêtre (croix ou Quitter)
    def closeEvent(self, event):
        if self.thread_mqtt is not None:
            self.disconnectMQTT()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())