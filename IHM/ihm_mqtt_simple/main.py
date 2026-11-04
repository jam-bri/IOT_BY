import sys

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QMainWindow

from client_mqtt import ClientMQTT
from thread_mqtt import ThreadMQTT
from mon_ihm import Ui_MainWindow

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
        self.btnDisconnect.clicked.connect(self.disconnectMQTT)
        self.actionQuit.triggered.connect(self.close)

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