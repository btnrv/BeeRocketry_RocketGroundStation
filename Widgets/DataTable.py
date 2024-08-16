from PySide6.QtWidgets import QApplication, QLabel, QGridLayout, QVBoxLayout, QWidget
from PySide6.QtCore import Qt

class DataPacket:
    def __init__(self):
        self.irtifa = 0.0
        self.gpsIrtifa = 0.0
        self.gpsEnlem = 39.81890428624599 
        self.gpsBoylam = 32.56358312070704
        self.gorevYukuIrtifa = 0.0
        self.gorevYukuEnlem = 39.81890428624599 
        self.gorevYukuBoylam = 32.56358312070704
        self.jiroskopX = 0.0
        self.jiroskopY = 0.0
        self.jiroskopZ = 0.0
        self.ivmeX = 0.0
        self.ivmeY = 0.0
        self.ivmeZ = 0.0
        self.aci = 0.0
        self.yaw = 0
        self.roll = 0
        self.pitch = 0
        self.nem = 0
        self.sicaklik = 0
        self.durum = 0
        self.packets = 0
        self.checksum = 0
        self.ivmeTotal = 0
        
    def assign_values(self, values):
        if len(values) != 21:
            raise ValueError("Malformed packet (necessary values not matching the amount)")
        self.irtifa, self.gpsIrtifa, self.gpsEnlem, self.gpsBoylam, self.gorevYukuIrtifa, self.gorevYukuEnlem, self.gorevYukuBoylam, self.jiroskopX, self.jiroskopY, self.jiroskopZ, self.ivmeX, self.ivmeY, self.ivmeZ, self.aci, self.yaw, self.roll, self.pitch, self.nem, self.sicaklik, self.durum, self.packets = map(float, values[:21])
        self.calculate_checksum()

    def calculate_checksum(self):
        total = (self.irtifa + self.gpsIrtifa + self.gpsEnlem + self.gpsBoylam +
                 self.gorevYukuIrtifa + self.gorevYukuEnlem + self.gorevYukuBoylam +
                 self.jiroskopX + self.jiroskopY + self.jiroskopZ +
                 self.ivmeX + self.ivmeY + self.ivmeZ +
                 self.aci + self.durum)
        self.checksum = int(total) % 256

class DataTable(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #201702;")
        
        # Create the title label
        self.title_label = QLabel("Data Packet Information")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFixedHeight(40)
        self.title_label.setStyleSheet("background-color: #fdb513; font-size: 20px; font-weight: bold; font-family: EncodeSans; color: #201702; padding: 5px;")
        
        # Create labels for each data point
        self.labels = {}
        self.data_names = [
            "Irtifa", "GPS Irtifa", "GPS Enlem", "GPS Boylam",
            "Gorev Yuku Irtifa", "Gorev Yuku Enlem", "Gorev Yuku Boylam",
            "Jiroskop X", "Jiroskop Y", "Jiroskop Z",
            "Ivme X", "Ivme Y", "Ivme Z",
            "Aci", "Yaw", "Roll", "Pitch",
            "Nem", "Sicaklik", "Durum", "Packets", "Checksum",
            "Paraşüt 1", "Paraşüt 2"  # New labels
        ]
        
        # Create grid layout
        self.grid_layout = QGridLayout()
        
        # Create and add labels to layout
        row = 0
        col = 0
        for name in self.data_names:
            label = QLabel(f"{name}: 0.0")
            label.setStyleSheet("font-size: 16px; font-weight: medium; font-family: EncodeSans; color: #fff; padding: 5px;")
            self.labels[name] = label
            self.grid_layout.addWidget(label, row, col)
            row += 1
            if row > 7:  # Change column every 8 rows for 3 columns layout
                row = 0
                col += 1
                if col >= 3:  # Reset to column 0 if exceeded 3 columns
                    col = 0

        # Create border widget
        self.border_widget = QWidget()
        self.border_widget.setStyleSheet("border: 2px solid #fdb513; border-radius: 5px; padding: 10px;")
        self.border_layout = QVBoxLayout(self.border_widget)
        self.border_layout.addWidget(self.title_label)
        self.border_layout.addLayout(self.grid_layout)
        
        # Create main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.border_widget)
        self.setLayout(self.main_layout)

        # Set initial styles for new labels
        self.labels["Paraşüt 1"].setStyleSheet("font-size: 18px; font-weight: bold; font-family: EncodeSans; color: #fff; padding: 5px; border: 0px;")
        self.labels["Paraşüt 2"].setStyleSheet("font-size: 18px; font-weight: bold; font-family: EncodeSans; color: #fff; padding: 5px; border: 0px;")

    def update_data(self, packet):
        # Update labels with data from DataPacket
        self.labels["Irtifa"].setText(f"Irtifa: {packet.irtifa:.2f}")
        self.labels["GPS Irtifa"].setText(f"GPS Irtifa: {packet.gpsIrtifa:.2f}")
        self.labels["GPS Enlem"].setText(f"GPS Enlem: {packet.gpsEnlem:.2f}")
        self.labels["GPS Boylam"].setText(f"GPS Boylam: {packet.gpsBoylam:.2f}")
        self.labels["Gorev Yuku Irtifa"].setText(f"Gorev Yuku Irtifa: {packet.gorevYukuIrtifa:.2f}")
        self.labels["Gorev Yuku Enlem"].setText(f"Gorev Yuku Enlem: {packet.gorevYukuEnlem:.2f}")
        self.labels["Gorev Yuku Boylam"].setText(f"Gorev Yuku Boylam: {packet.gorevYukuBoylam:.2f}")
        self.labels["Jiroskop X"].setText(f"Jiroskop X: {packet.jiroskopX:.2f}")
        self.labels["Jiroskop Y"].setText(f"Jiroskop Y: {packet.jiroskopY:.2f}")
        self.labels["Jiroskop Z"].setText(f"Jiroskop Z: {packet.jiroskopZ:.2f}")
        self.labels["Ivme X"].setText(f"Ivme X: {packet.ivmeX:.2f}")
        self.labels["Ivme Y"].setText(f"Ivme Y: {packet.ivmeY:.2f}")
        self.labels["Ivme Z"].setText(f"Ivme Z: {packet.ivmeZ:.2f}")
        self.labels["Aci"].setText(f"Aci: {packet.aci:.2f}")
        self.labels["Yaw"].setText(f"Yaw: {packet.yaw:.2f}")
        self.labels["Roll"].setText(f"Roll: {packet.roll:.2f}")
        self.labels["Pitch"].setText(f"Pitch: {packet.pitch:.2f}")
        self.labels["Nem"].setText(f"Nem: {packet.nem:.2f}")
        self.labels["Sicaklik"].setText(f"Sicaklik: {packet.sicaklik:.2f}")
        self.labels["Durum"].setText(f"Durum: {packet.durum}")
        self.labels["Packets"].setText(f"Packets: {packet.packets}")
        self.labels["Checksum"].setText(f"Checksum: {packet.checksum}")

        # Update the new labels based on durum
        durum = packet.durum
        if durum == 1:
            self.labels["Paraşüt 1"].setText("1. Paraşüt Kapalı")
            self.labels["Paraşüt 2"].setText("2. Paraşüt Kapalı")
            self.labels["Paraşüt 1"].setStyleSheet("font-size: 18px; font-weight: bold; font-family: EncodeSans; color: #dd1113; padding: 5px; border: 0px;")
            self.labels["Paraşüt 2"].setStyleSheet("font-size: 18px; font-weight: bold; font-family: EncodeSans; color: #dd1113; padding: 5px; border: 0px;")
        elif durum == 2:
            self.labels["Paraşüt 1"].setText("1. Paraşüt Açık")
            self.labels["Paraşüt 2"].setText("2. Paraşüt Kapalı")
            self.labels["Paraşüt 1"].setStyleSheet("font-size: 18px; font-weight: bold; font-family: EncodeSans; color: #5bfd13; padding: 5px; border: 0px;")
            self.labels["Paraşüt 2"].setStyleSheet("font-size: 18px; font-weight: bold; font-family: EncodeSans; color: #dd1113; padding: 5px; border: 0px;")
        elif durum == 3:
            self.labels["Paraşüt 1"].setText("1. Paraşüt Kapalı")
            self.labels["Paraşüt 2"].setText("2. Paraşüt Açık")
            self.labels["Paraşüt 1"].setStyleSheet("font-size: 18px; font-weight: bold; font-family: EncodeSans; color: #dd1113; padding: 5px; border: 0px;")
            self.labels["Paraşüt 2"].setStyleSheet("font-size: 18px; font-weight: bold; font-family: EncodeSans; color: #5bfd13; padding: 5px; border: 0px;")
        elif durum == 4:
            self.labels["Paraşüt 1"].setText("1. Paraşüt Açık")
            self.labels["Paraşüt 2"].setText("2. Paraşüt Açık")
            self.labels["Paraşüt 1"].setStyleSheet("font-size: 18px; font-weight: bold; font-family: EncodeSans; color: #5bfd13; padding: 5px; border: 0px;")
            self.labels["Paraşüt 2"].setStyleSheet("font-size: 18px; font-weight: bold; font-family: EncodeSans; color: #5bfd13; padding: 5px; border: 0px;")

if __name__ == "__main__":
    app = QApplication([])
    widget = DataTable()
    widget.show()
    
    app.exec()
