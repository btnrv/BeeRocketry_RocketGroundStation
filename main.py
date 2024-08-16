import os
import sys
import signal
import time
from dotenv import load_dotenv
from pathlib import Path

from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

from Widgets.DataTable import DataTable
from Widgets.AccelerationDisplay import AccelerationDisplay
from Widgets.Altitude import Altitude
from Widgets.PackageInfo import PackageInfo
from Widgets.Status import Status
from Widgets.MapGPS import MapGPS
from Widgets.Image import ImageDisplay
from Widgets.Serial import SerialWidget, DataPacket
from Widgets.ThreeDimensionalXYZ import ThreeDimensionalXyzWidget
from Widgets.RYP import RollYawPitchWidget

# ! BeeRocketry 2024 Teknofest Roket Yarışması ! #

class RocketInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Initialize values
        load_dotenv()
        self.graphsUpdateTime = int(os.getenv('GRAPHS_UPDATE_TIMER'))
        self.mapsUpdateTime = int(os.getenv('MAPS_UPDATE_TIMER'))
        self.packets = 0
        self.lastUpdate = time.time()
        
        # Main Window Settings
        self.setWindowTitle("BeeRocketry Ground Station")
        self.setObjectName("main_window")
        icon_path = Path(__file__).parent / "Assets" / "logo.png"
        self.setWindowIcon(QIcon(str(icon_path)))

        self.main_widget = QWidget(self)
        self.main_widget.setStyleSheet("""
            QWidget#statuses_widget {
                background-color: #201702; margin:0px; padding:0px; border: 1px solid #fdb513;
            }
            QMainWindow#main_window {
                background-color: #000; border: 1px solid #fdb513; border-radius: 5px;
            }
        """)
        self.setCentralWidget(self.main_widget)

        # Widgets
        self.rypGraph = RollYawPitchWidget()
        self.xyzAccel = AccelerationDisplay("Acceleration")
        self.xyzGyro = ThreeDimensionalXyzWidget("Gyroscope")
        self.rocketAltitude = Altitude("Rocket", color="#00ffff")
        self.packageAltitude = Altitude("Package", color="#006fff")
        self.statusDisplay = Status("Datas")
        self.dataTableWidget = DataTable()
        self.rocketMapWidget = MapGPS("Rocket")
        self.packageMapWidget = MapGPS("Package")

        self.mapsTitle = QLabel("Rocket and Package Maps")
        self.mapsTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mapsTitle.setStyleSheet("""
            background-color: #fdb513; font-size: 20px; font-weight: bold; font-family: EncodeSans; color: #201702;
        """)
        self.mapsTitle.setFixedHeight(40)
        self.mapsWidget = QWidget()
        self.mapsWidgetLayout = QGridLayout()
        self.mapsLayout = QGridLayout()
        self.mapsWidget.setLayout(self.mapsWidgetLayout)
        self.mapsLayout.addWidget(self.rocketMapWidget, 0, 0)
        self.mapsLayout.addWidget(self.packageMapWidget, 0, 1)
        self.mapsWidgetLayout.addWidget(self.mapsTitle, 0, 0)
        self.mapsWidgetLayout.addLayout(self.mapsLayout, 1 , 0)
        self.mapsWidget.setStyleSheet("""
            background-color: #201702; border: 2px solid #fdb513; border-radius: 5px;
        """)

        self.packageInfoWidget = PackageInfo()
        self.logoWidget = ImageDisplay()
        self.serialWidget = SerialWidget()
        self.resetButton = QPushButton("Reset Overlay")
        self.resetButton.clicked.connect(self.reset_overlay)
        self.resetButton.setStyleSheet("""
            background-color: #fdb513; font-size: 15px; border-radius: 5px; font-weight: bold; font-family: EncodeSans; color: #201702;
        """)
        self.resetButton.setFixedHeight(25)
        self.resetButton.setFixedWidth(150)

        # Layouts
        self.main_layout = QGridLayout(self.main_widget)
        self.left_layout = QGridLayout()
        self.left_layout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.right_layout = QGridLayout()
        self.right_bottom_layout = QGridLayout()

        self.moistureTemperatureLayout = QGridLayout()
        self.status_layout = QHBoxLayout()
        self.statuses_widget = QWidget()
        self.statuses_widget.setLayout(self.status_layout)
        self.statuses_widget.setObjectName("statuses_widget")
        self.right_layout_widget = QWidget()
        self.right_layout_widget.setObjectName("right_layout_widget")
        self.right_layout_widget.setLayout(self.right_layout)

        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setColumnStretch(0, 4)
        self.main_layout.setColumnStretch(1, 3)

        self.left_layout.setSpacing(0)
        self.right_layout.setSpacing(0)

        self.main_layout.addLayout(self.left_layout, 0, 0)
        self.main_layout.addWidget(self.right_layout_widget, 0, 1)
        
        self.left_layout.addWidget(self.rypGraph, 0, 0)
        self.left_layout.addWidget(self.packageInfoWidget, 0, 1)
        self.left_layout.addWidget(self.xyzAccel, 1, 0)
        self.left_layout.addWidget(self.xyzGyro, 1, 1)
        self.left_layout.addWidget(self.rocketAltitude, 2, 0)
        self.left_layout.addWidget(self.packageAltitude, 2, 1)
        
        self.status_layout.addWidget(self.statusDisplay)
        self.serialAndLogoLayout = QGridLayout()
        self.serialAndLogoLayout.addWidget(self.serialWidget, 0, 0, Qt.AlignmentFlag.AlignVCenter)
        self.serialAndLogoLayout.addWidget(self.logoWidget, 0, 1, )

        self.right_layout.addWidget(self.mapsWidget, 0, 0)
        self.right_layout.addWidget(self.dataTableWidget, 1, 0)
        self.right_layout.addLayout(self.serialAndLogoLayout, 2, 0, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft)
        self.right_layout.addWidget(self.resetButton, 3, 0, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignCenter)
        self.right_layout.setRowStretch(0, 2)
        self.right_layout.setRowStretch(1, 4)
        self.right_layout.setRowStretch(2, 2)
        self.right_layout.setRowStretch(3, 0)
        
        # Serial Reader Signal
        self.serialWidget.data_packet_signal.connect(self.update_data)
        self.maptimer = time.time()

    def update_data(self, dataPacket: DataPacket):
        # Data table updates live
        self.dataTableWidget.update_data(dataPacket)
        if not time.time() - self.lastUpdate >= self.graphsUpdateTime:
            pass
        else:
            self.rocketAltitude.update(dataPacket.irtifa)
            self.packageAltitude.update(dataPacket.gorevYukuIrtifa)
            self.statusDisplay.update(dataPacket.durum)
            self.xyzAccel.update(dataPacket.ivmeX, dataPacket.ivmeY, dataPacket.ivmeZ, dataPacket.ivmeTotal)
            self.xyzGyro.update(dataPacket.jiroskopX, dataPacket.jiroskopY, dataPacket.jiroskopZ)
            self.rypGraph.update(dataPacket.roll, dataPacket.yaw, dataPacket.pitch)
            if time.time() - self.maptimer >= self.mapsUpdateTime:
                self.rocketMapWidget.update([dataPacket.gpsEnlem, dataPacket.gpsBoylam])
                self.packageMapWidget.update([dataPacket.gorevYukuEnlem, dataPacket.gorevYukuBoylam])
                self.maptimer = time.time()
            self.statusDisplay.update(status_code=dataPacket.durum)
            self.packageInfoWidget.update(dataPacket.nem, dataPacket.sicaklik)
            self.lastUpdate = time.time()

    def reset_overlay(self):
        self.serialWidget.stop_transfer()
        self.xyzAccel.reset()
        self.xyzGyro.reset()
        self.rocketAltitude.reset()
        self.packageAltitude.reset()
        self.rypGraph.reset()
        self.packageInfoWidget.reset()
        self.update_data(DataPacket())

def handle_keyboard_interrupt(signum, frame):
    rocket_interface.serialWidget.stop_transfer()
    QApplication.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    signal.signal(signal.SIGINT, handle_keyboard_interrupt)
    rocket_interface = RocketInterface()
    rocket_interface.showMaximized()
    sys.exit(app.exec())