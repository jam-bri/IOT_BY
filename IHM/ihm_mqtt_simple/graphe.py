# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'graphe.ui'
##
## Created by: Qt User Interface Compiler version 6.12.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDateTimeEdit, QDialog,
    QDialogButtonBox, QGraphicsView, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_GraphWindow(object):
    def setupUi(self, GraphWindow):
        if not GraphWindow.objectName():
            GraphWindow.setObjectName(u"GraphWindow")
        GraphWindow.resize(700, 560)
        self.verticalLayout = QVBoxLayout(GraphWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.layoutDates = QHBoxLayout()
        self.layoutDates.setObjectName(u"layoutDates")
        self.lblDebut = QLabel(GraphWindow)
        self.lblDebut.setObjectName(u"lblDebut")

        self.layoutDates.addWidget(self.lblDebut)

        self.dteStartTime = QDateTimeEdit(GraphWindow)
        self.dteStartTime.setObjectName(u"dteStartTime")

        self.layoutDates.addWidget(self.dteStartTime)

        self.lblFin = QLabel(GraphWindow)
        self.lblFin.setObjectName(u"lblFin")

        self.layoutDates.addWidget(self.lblFin)

        self.dteEndTime = QDateTimeEdit(GraphWindow)
        self.dteEndTime.setObjectName(u"dteEndTime")

        self.layoutDates.addWidget(self.dteEndTime)


        self.verticalLayout.addLayout(self.layoutDates)

        self.graphicsView = QGraphicsView(GraphWindow)
        self.graphicsView.setObjectName(u"graphicsView")

        self.verticalLayout.addWidget(self.graphicsView)

        self.layoutBoutons = QHBoxLayout()
        self.layoutBoutons.setObjectName(u"layoutBoutons")
        self.btnClearData = QPushButton(GraphWindow)
        self.btnClearData.setObjectName(u"btnClearData")

        self.layoutBoutons.addWidget(self.btnClearData)

        self.btnLoadData = QPushButton(GraphWindow)
        self.btnLoadData.setObjectName(u"btnLoadData")

        self.layoutBoutons.addWidget(self.btnLoadData)


        self.verticalLayout.addLayout(self.layoutBoutons)

        self.buttonBox = QDialogButtonBox(GraphWindow)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Close)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(GraphWindow)
        self.buttonBox.rejected.connect(GraphWindow.reject)

        QMetaObject.connectSlotsByName(GraphWindow)
    # setupUi

    def retranslateUi(self, GraphWindow):
        GraphWindow.setWindowTitle(QCoreApplication.translate("GraphWindow", u"Courbes du capteur", None))
        self.lblDebut.setText(QCoreApplication.translate("GraphWindow", u"D\u00e9but", None))
        self.dteStartTime.setDisplayFormat(QCoreApplication.translate("GraphWindow", u"yyyy-MM-dd HH:mm:ss", None))
        self.lblFin.setText(QCoreApplication.translate("GraphWindow", u"Fin", None))
        self.dteEndTime.setDisplayFormat(QCoreApplication.translate("GraphWindow", u"yyyy-MM-dd HH:mm:ss", None))
        self.btnClearData.setText(QCoreApplication.translate("GraphWindow", u"Effacer les courbes", None))
        self.btnLoadData.setText(QCoreApplication.translate("GraphWindow", u"Charger les donn\u00e9es", None))
    # retranslateUi

