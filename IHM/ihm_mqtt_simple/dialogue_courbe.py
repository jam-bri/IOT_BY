import sqlite3
from datetime import datetime

from PySide6.QtCore import QDateTime
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QGraphicsScene, QDialog, QGraphicsPixmapItem
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg

from graphe import Ui_GraphWindow

database_name = "IOT.db"
table_name = "IOT_DATA"


class CourbeDialog(QDialog, Ui_GraphWindow):
    def __init__(self, id_pc):
        super().__init__()
        self.setupUi(self)
        self.id_pc = id_pc

        # par défaut : la dernière heure
        dte = QDateTime.currentDateTime()
        dts = dte.addSecs(-3600)
        self.dteStartTime.setDateTime(dts)
        self.dteEndTime.setDateTime(dte)

        self.scene = QGraphicsScene()
        self.graphicsView.setScene(self.scene)

        self.btnLoadData.clicked.connect(self.afficher_courbe)
        self.btnClearData.clicked.connect(self.effacer_courbe)

    # transforme une figure matplotlib en image Qt
    def figure_to_pixmap(self, fig):
        canvas = FigureCanvasAgg(fig)
        canvas.draw()
        width, height = canvas.get_width_height()
        image = QImage(canvas.buffer_rgba(), width, height, QImage.Format_RGBA8888)
        return QPixmap.fromImage(image.copy())

    def afficher_courbe(self):
        # les deux champs sont au format yyyy-MM-dd HH:mm:ss, comme les dates de la base
        debut = self.dteStartTime.text()
        fin = self.dteEndTime.text()

        conn = sqlite3.connect(database_name)
        cur = conn.cursor()
        cur.execute(f"CREATE TABLE IF NOT EXISTS {table_name} "
                    "(Id_capteur integer, Date text, Version text, Temperature real, Humidite real)")
        cur.execute(f"SELECT Date, Temperature, Humidite FROM {table_name} "
                    "WHERE Id_capteur = ? AND Date BETWEEN ? AND ? ORDER BY Date ASC",
                    (self.id_pc, debut, fin))
        rows = cur.fetchall()
        conn.close()

        self.scene.clear()
        if not rows:
            self.scene.addText("Aucune donnée sur cette période")
            return

        date_x = [datetime.strptime(r[0], "%Y-%m-%d %H:%M:%S") for r in rows]
        temp_y = [r[1] for r in rows]
        humi_y = [r[2] for r in rows]

        fig = Figure(figsize=(6.5, 4), dpi=100)
        ax = fig.add_subplot()
        ax.plot(date_x, temp_y, marker="o", markersize=3, label="Température (°C)")
        ax.plot(date_x, humi_y, marker="+", label="Humidité (%)")
        ax.set_title(f"Données capteur IdO {self.id_pc} ({len(rows)} mesures)")
        ax.set_xlabel("Heure")
        ax.set_ylabel("Valeurs")
        ax.grid(True)
        ax.legend()
        fig.autofmt_xdate()

        self.scene.addItem(QGraphicsPixmapItem(self.figure_to_pixmap(fig)))

    def effacer_courbe(self):
        self.scene.clear()