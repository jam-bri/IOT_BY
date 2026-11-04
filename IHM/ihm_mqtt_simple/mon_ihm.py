# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mon_ihm.ui'
##
## Created by: Qt User Interface Compiler version 6.12.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QGroupBox, QLabel,
    QLineEdit, QMainWindow, QMenu, QMenuBar,
    QPushButton, QSizePolicy, QStatusBar, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(620, 520)
        self.actionQuit = QAction(MainWindow)
        self.actionQuit.setObjectName(u"actionQuit")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.grpConnexion = QGroupBox(self.centralwidget)
        self.grpConnexion.setObjectName(u"grpConnexion")
        self.gridConnexion = QGridLayout(self.grpConnexion)
        self.gridConnexion.setObjectName(u"gridConnexion")
        self.lblBroker = QLabel(self.grpConnexion)
        self.lblBroker.setObjectName(u"lblBroker")

        self.gridConnexion.addWidget(self.lblBroker, 0, 0, 1, 1)

        self.lneBroker = QLineEdit(self.grpConnexion)
        self.lneBroker.setObjectName(u"lneBroker")

        self.gridConnexion.addWidget(self.lneBroker, 0, 1, 1, 1)

        self.lblPort = QLabel(self.grpConnexion)
        self.lblPort.setObjectName(u"lblPort")

        self.gridConnexion.addWidget(self.lblPort, 0, 2, 1, 1)

        self.lnePort = QLineEdit(self.grpConnexion)
        self.lnePort.setObjectName(u"lnePort")

        self.gridConnexion.addWidget(self.lnePort, 0, 3, 1, 1)

        self.lblId = QLabel(self.grpConnexion)
        self.lblId.setObjectName(u"lblId")

        self.gridConnexion.addWidget(self.lblId, 1, 0, 1, 1)

        self.lneIdCapteur = QLineEdit(self.grpConnexion)
        self.lneIdCapteur.setObjectName(u"lneIdCapteur")

        self.gridConnexion.addWidget(self.lneIdCapteur, 1, 1, 1, 1)

        self.btnConnect = QPushButton(self.grpConnexion)
        self.btnConnect.setObjectName(u"btnConnect")

        self.gridConnexion.addWidget(self.btnConnect, 1, 2, 1, 1)

        self.btnDisconnect = QPushButton(self.grpConnexion)
        self.btnDisconnect.setObjectName(u"btnDisconnect")

        self.gridConnexion.addWidget(self.btnDisconnect, 1, 3, 1, 1)


        self.verticalLayout.addWidget(self.grpConnexion)

        self.grpMesures = QGroupBox(self.centralwidget)
        self.grpMesures.setObjectName(u"grpMesures")
        self.gridMesures = QGridLayout(self.grpMesures)
        self.gridMesures.setObjectName(u"gridMesures")
        self.lblTitreVersion = QLabel(self.grpMesures)
        self.lblTitreVersion.setObjectName(u"lblTitreVersion")

        self.gridMesures.addWidget(self.lblTitreVersion, 0, 0, 1, 1)

        self.lblVersion = QLabel(self.grpMesures)
        self.lblVersion.setObjectName(u"lblVersion")

        self.gridMesures.addWidget(self.lblVersion, 0, 1, 1, 1)

        self.lblTitreDate = QLabel(self.grpMesures)
        self.lblTitreDate.setObjectName(u"lblTitreDate")

        self.gridMesures.addWidget(self.lblTitreDate, 1, 0, 1, 1)

        self.lblDate = QLabel(self.grpMesures)
        self.lblDate.setObjectName(u"lblDate")

        self.gridMesures.addWidget(self.lblDate, 1, 1, 1, 1)

        self.lblTitreTemp = QLabel(self.grpMesures)
        self.lblTitreTemp.setObjectName(u"lblTitreTemp")

        self.gridMesures.addWidget(self.lblTitreTemp, 2, 0, 1, 1)

        self.lblTemperature = QLabel(self.grpMesures)
        self.lblTemperature.setObjectName(u"lblTemperature")
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.lblTemperature.setFont(font)

        self.gridMesures.addWidget(self.lblTemperature, 2, 1, 1, 1)

        self.lblTitreHum = QLabel(self.grpMesures)
        self.lblTitreHum.setObjectName(u"lblTitreHum")

        self.gridMesures.addWidget(self.lblTitreHum, 3, 0, 1, 1)

        self.lblHumidity = QLabel(self.grpMesures)
        self.lblHumidity.setObjectName(u"lblHumidity")
        self.lblHumidity.setFont(font)

        self.gridMesures.addWidget(self.lblHumidity, 3, 1, 1, 1)


        self.verticalLayout.addWidget(self.grpMesures)

        self.grpCommandes = QGroupBox(self.centralwidget)
        self.grpCommandes.setObjectName(u"grpCommandes")
        self.gridCommandes = QGridLayout(self.grpCommandes)
        self.gridCommandes.setObjectName(u"gridCommandes")
        self.btnSynchroDateTime = QPushButton(self.grpCommandes)
        self.btnSynchroDateTime.setObjectName(u"btnSynchroDateTime")

        self.gridCommandes.addWidget(self.btnSynchroDateTime, 0, 0, 1, 1)

        self.btnStartMeasure = QPushButton(self.grpCommandes)
        self.btnStartMeasure.setObjectName(u"btnStartMeasure")

        self.gridCommandes.addWidget(self.btnStartMeasure, 0, 1, 1, 1)

        self.btnStopMeasure = QPushButton(self.grpCommandes)
        self.btnStopMeasure.setObjectName(u"btnStopMeasure")

        self.gridCommandes.addWidget(self.btnStopMeasure, 0, 2, 1, 1)

        self.btnSlowBlink = QPushButton(self.grpCommandes)
        self.btnSlowBlink.setObjectName(u"btnSlowBlink")

        self.gridCommandes.addWidget(self.btnSlowBlink, 1, 0, 1, 1)

        self.btnFastBlink = QPushButton(self.grpCommandes)
        self.btnFastBlink.setObjectName(u"btnFastBlink")

        self.gridCommandes.addWidget(self.btnFastBlink, 1, 1, 1, 1)

        self.btnGraph = QPushButton(self.grpCommandes)
        self.btnGraph.setObjectName(u"btnGraph")

        self.gridCommandes.addWidget(self.btnGraph, 1, 2, 1, 1)

        self.lblPeriode = QLabel(self.grpCommandes)
        self.lblPeriode.setObjectName(u"lblPeriode")

        self.gridCommandes.addWidget(self.lblPeriode, 2, 0, 1, 1)

        self.lnePeriod = QLineEdit(self.grpCommandes)
        self.lnePeriod.setObjectName(u"lnePeriod")

        self.gridCommandes.addWidget(self.lnePeriod, 2, 1, 1, 1)

        self.btnBlink = QPushButton(self.grpCommandes)
        self.btnBlink.setObjectName(u"btnBlink")

        self.gridCommandes.addWidget(self.btnBlink, 2, 2, 1, 1)

        self.lblBargraph = QLabel(self.grpCommandes)
        self.lblBargraph.setObjectName(u"lblBargraph")

        self.gridCommandes.addWidget(self.lblBargraph, 3, 0, 1, 1)

        self.lneBargraph = QLineEdit(self.grpCommandes)
        self.lneBargraph.setObjectName(u"lneBargraph")

        self.gridCommandes.addWidget(self.lneBargraph, 3, 1, 1, 2)


        self.verticalLayout.addWidget(self.grpCommandes)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menuFichier = QMenu(self.menubar)
        self.menuFichier.setObjectName(u"menuFichier")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFichier.menuAction())
        self.menuFichier.addAction(self.actionQuit)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"IHM capteur IdO TempHumiX", None))
        self.actionQuit.setText(QCoreApplication.translate("MainWindow", u"Quitter", None))
        self.grpConnexion.setTitle(QCoreApplication.translate("MainWindow", u"Connexion au broker", None))
        self.lblBroker.setText(QCoreApplication.translate("MainWindow", u"Broker", None))
        self.lneBroker.setText(QCoreApplication.translate("MainWindow", u"127.0.0.1", None))
        self.lblPort.setText(QCoreApplication.translate("MainWindow", u"Port", None))
        self.lnePort.setText(QCoreApplication.translate("MainWindow", u"1883", None))
        self.lblId.setText(QCoreApplication.translate("MainWindow", u"Id capteur", None))
        self.lneIdCapteur.setText(QCoreApplication.translate("MainWindow", u"42914", None))
        self.btnConnect.setText(QCoreApplication.translate("MainWindow", u"Connecter", None))
        self.btnDisconnect.setText(QCoreApplication.translate("MainWindow", u"D\u00e9connecter", None))
        self.grpMesures.setTitle(QCoreApplication.translate("MainWindow", u"Donn\u00e9es du capteur", None))
        self.lblTitreVersion.setText(QCoreApplication.translate("MainWindow", u"Version", None))
        self.lblVersion.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.lblTitreDate.setText(QCoreApplication.translate("MainWindow", u"Date / heure", None))
        self.lblDate.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.lblTitreTemp.setText(QCoreApplication.translate("MainWindow", u"Temp\u00e9rature", None))
        self.lblTemperature.setText(QCoreApplication.translate("MainWindow", u"- \u00b0C", None))
        self.lblTitreHum.setText(QCoreApplication.translate("MainWindow", u"Humidit\u00e9", None))
        self.lblHumidity.setText(QCoreApplication.translate("MainWindow", u"- %", None))
        self.grpCommandes.setTitle(QCoreApplication.translate("MainWindow", u"Commandes", None))
        self.btnSynchroDateTime.setText(QCoreApplication.translate("MainWindow", u"Mise \u00e0 l'heure", None))
        self.btnStartMeasure.setText(QCoreApplication.translate("MainWindow", u"D\u00e9marrer mesure", None))
        self.btnStopMeasure.setText(QCoreApplication.translate("MainWindow", u"Arr\u00eater mesure", None))
        self.btnSlowBlink.setText(QCoreApplication.translate("MainWindow", u"Clignotement lent", None))
        self.btnFastBlink.setText(QCoreApplication.translate("MainWindow", u"Clignotement rapide", None))
        self.btnGraph.setText(QCoreApplication.translate("MainWindow", u"Courbes...", None))
        self.lblPeriode.setText(QCoreApplication.translate("MainWindow", u"P\u00e9riode (ms)", None))
        self.lnePeriod.setText(QCoreApplication.translate("MainWindow", u"1000", None))
        self.btnBlink.setText(QCoreApplication.translate("MainWindow", u"Clignotement perso", None))
        self.lblBargraph.setText(QCoreApplication.translate("MainWindow", u"Bargraphe (0-1023)", None))
        self.lneBargraph.setPlaceholderText(QCoreApplication.translate("MainWindow", u"valeur puis Entr\u00e9e", None))
        self.menuFichier.setTitle(QCoreApplication.translate("MainWindow", u"Fichier", None))
    # retranslateUi

