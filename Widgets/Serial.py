from PySide6.QtWidgets import *
from PySide6.QtCore import *
import sys
import threading
import serial
import struct
from dotenv import load_dotenv
import os
import serial.tools.list_ports

load_dotenv()

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
        self.yaw = 0.0
        self.roll = 0.0
        self.pitch = 0.0
        self.nem = 0.0
        self.sicaklik = 0.0
        self.durum = 0
        self.packets = 0
        self.checksum = 0
        self.ivmeTotal = 0
        self.kademeIrtifa = 0.0
        self.kademeEnlem = 0.0
        self.kademeBoylam = 0.0
        
    def assign_values(self, values):
        # ! Warning: You have to edit this part according to your data packet string
        # ! Our category does not include Kademe data, so the value is 22. If yours does, set to 25 etc.
        # ! Otherwise incomplete packets will pass and throw out errors, stopping serial comms.
        if len(values) != 22:
            pass
        else:
            self.irtifa = float(values[0])
            self.gpsIrtifa = float(values[1])
            self.gpsEnlem = float(values[2])
            self.gpsBoylam = float(values[3])
            self.gorevYukuIrtifa = float(values[4])
            self.gorevYukuEnlem = float(values[5])
            self.gorevYukuBoylam = float(values[6])
            self.jiroskopX = float(values[7])
            self.jiroskopY = float(values[8])
            self.jiroskopZ = float(values[9])
            self.ivmeX = float(values[10])
            self.ivmeY = float(values[11])
            self.ivmeZ = float(values[12])
            self.aci = float(values[13])
            self.yaw = float(values[14])
            self.roll = float(values[15])
            self.pitch = float(values[16])
            self.nem = float(values[17])
            self.sicaklik = float(values[18])
            self.durum = int(values[19])
            self.packets = int(values[20])
            self.ivmeTotal = float(values[21])
            print(self.__dict__)

def float_to_bytes(value):
    return struct.pack('f', value)

def calculate_checksum(packet):
    checksum = sum(packet[4:75]) % 256
    return checksum

class SerialWidget(QWidget):
    data_packet_signal = Signal(DataPacket)
    def __init__(self):
        super().__init__()

        self.takimID = int(os.getenv('TAKIM_ID'))
        self.dataPacket = DataPacket()
        self.serial_reading = None
        self.serial_sending = None
        self.setObjectName("serialWidget")
        self.setStyleSheet("""QWidget#subWidget {
                            background-color: #201702; border: 2px solid #fdb513; border-radius: 5px; padding: 5px;
                           }
                           QWidget#deviceSettings {
                            background-color: #201702; border: 2px solid #fdb513; border-radius: 5px; padding: 5px;
                           }
                           """)
        self.subWidget = QWidget()
        self.subWidget.setObjectName("subWidget")
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.subWidget)
        self.setLayout(main_layout)

        sub_layout = QVBoxLayout()
        self.subWidget.setLayout(sub_layout)

        self.title_label = QLabel("Data  Transfer  Settings")
        self.title_label.setStyleSheet("background-color: #fdb513; font-size: 20px; border-radius: 5px; font-weight: bold; font-family: EncodeSans; color: #201702;")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFixedHeight(40)
        sub_layout.addWidget(self.title_label)

        # Data Reading Device Dropdown
        self.data_reading_layout = QGridLayout()
        self.data_reading_device = QComboBox()
        self.data_reading_device.addItem("Select device...")
        self.data_reading_device.addItems(self.list_com_ports())
        self.data_reading_device.setStyleSheet("border: 1px solid #fdb513; border-radius: 5px; margin: 4px; padding: 4px; background-color: #201702; font-size: 16px; font-weight: normal; font-family: EncodeSans; color: #fff;")

        self.data_reading_widget = QWidget()
        self.data_reading_widget.setStyleSheet("border: 1px ;")
        self.data_reading_widget.setLayout(self.data_reading_layout)

        self.data_reading_label = QLabel("Reading Device:")
        self.data_reading_label.setStyleSheet("border: 0px; font-size: 20px; font-weight: bold; font-family: EncodeSans; color: #fff;")
        self.data_reading_layout.addWidget(self.data_reading_label, 0, 0)
        self.data_reading_layout.addWidget(self.data_reading_device, 0, 1)

        self.baudrate_reading = QComboBox()
        self.baudrate_reading.addItems(["9600", "19200", "38400", "57600", "115200"])
        self.baudrate_reading.setCurrentText("115200")
        self.baudrate_reading.setStyleSheet("border: 1px solid #fdb513; border-radius: 5px; margin: 8px; background-color: #201702; font-size: 10px; font-weight: normal; font-family: EncodeSans; color: #fff;")
        self.baudrate_reading_label = QLabel("BR:")
        self.baudrate_reading_label.setStyleSheet("border: 0px; font-size: 16px; font-weight: bold; font-family: EncodeSans; color: #fff;")
        self.data_reading_layout.addWidget(self.baudrate_reading_label, 0, 2)
        self.data_reading_layout.addWidget(self.baudrate_reading, 0, 3)

        self.data_sending_layout = QGridLayout()
        self.data_sending_device = QComboBox()
        self.data_sending_device.addItem("Select device...")
        self.data_sending_device.addItems(self.list_com_ports())
        self.data_sending_device.setStyleSheet("border: 1px solid #fdb513; border-radius: 5px; margin: 4px; padding: 4px; background-color: #201702; font-size: 16px; font-weight: normal; font-family: EncodeSans; color: #fff;")

        self.data_sending_widget = QWidget()
        self.data_sending_widget.setStyleSheet("border: 1px ;")
        self.data_sending_widget.setLayout(self.data_sending_layout)

        self.data_sending_label = QLabel("Sending Device:")
        self.data_sending_label.setStyleSheet("border: 0px; font-size: 20px; font-weight: bold; font-family: EncodeSans; color: #fff;")
        self.data_sending_layout.addWidget(self.data_sending_label, 0, 0)
        self.data_sending_layout.addWidget(self.data_sending_device, 0, 1)

        self.baudrate_sending = QComboBox()
        self.baudrate_sending.addItems(["9600", "19200", "38400", "57600", "115200"])
        self.baudrate_sending.setCurrentText("19200")
        self.baudrate_sending.setStyleSheet("border: 1px solid #fdb513; border-radius: 5px; margin: 8px; background-color: #201702; font-size: 10px; font-weight: normal; font-family: EncodeSans; color: #fff;")
        self.baudrate_sending_label = QLabel("BR:")
        self.baudrate_sending_label.setStyleSheet("border: 0px; font-size: 16px; font-weight: bold; font-family: EncodeSans; color: #fff;")
        self.data_sending_layout.addWidget(self.baudrate_sending_label, 0, 2)
        self.data_sending_layout.addWidget(self.baudrate_sending, 0, 3)

        # Add grid layout to main layout and place labels at the bottom
        sub_layout.addWidget(self.data_reading_widget)
        sub_layout.addWidget(self.data_sending_widget)

        self.setLayout(main_layout)

        self.buttonsLayout=QHBoxLayout()

        self.start_button = QPushButton("Start")
        self.start_button.setFixedHeight(30)
        self.start_button.clicked.connect(self.start_transfer)
        self.start_button.setStyleSheet("background-color: #fdb513; font-size: 12px; max-width: 150px; border-radius: 5px; font-weight: bold; font-family: EncodeSans; color: #201702;")
        self.stop_button = QPushButton("Stop")
        self.stop_button.setFixedHeight(30)
        self.stop_button.clicked.connect(self.stop_transfer)
        self.stop_button.setStyleSheet("background-color: #fdb513; font-size: 12px; max-width: 150px; border-radius: 5px; font-weight: bold; font-family: EncodeSans; color: #201702;")

        self.buttonsLayout.addWidget(self.start_button, Qt.AlignCenter)
        self.buttonsLayout.addWidget(self.stop_button, Qt.AlignCenter)

        sub_layout.addLayout(self.buttonsLayout)

    def list_com_ports(self):
        ports = serial.tools.list_ports.comports()
        return [f"{port.device[:5]} - {port.description[:18]}" for port in ports]

    def construct_send_packet(self):
        packet = bytearray(78)
        packet[0:4] = b'\xFF\xFF\x54\x52'  # Sabit
        packet[4] = self.takimID  # ! Takim ID
        packet[5] = int(self.dataPacket.packets)  # Sayac degeri
        packet[6:10] = float_to_bytes(self.dataPacket.irtifa)  # Irtifa degeri
        packet[10:14] = float_to_bytes(self.dataPacket.gpsIrtifa)  # Roket GPS Irtifa degeri
        packet[14:18] = float_to_bytes(self.dataPacket.gpsEnlem)  # Roket enlem degeri
        packet[18:22] = float_to_bytes(self.dataPacket.gpsBoylam)  # Roket boylam degeri
        packet[22:26] = float_to_bytes(self.dataPacket.gorevYukuIrtifa)  # Gorev yuku GPS Irtifa degeri
        packet[26:30] = float_to_bytes(self.dataPacket.gorevYukuEnlem)  # Gorev yuku enlem degeri
        packet[30:34] = float_to_bytes(self.dataPacket.gorevYukuBoylam)  # Gorev yuku boylam degeri
        packet[34:38] = float_to_bytes(self.dataPacket.kademeIrtifa)  # Kademe GPS Irtifa degeri
        packet[38:42] = float_to_bytes(self.dataPacket.kademeEnlem)  # Kademe enlem degeri
        packet[42:46] = float_to_bytes(self.dataPacket.kademeBoylam)  # Kademe boylam degeri
        packet[46:50] = float_to_bytes(self.dataPacket.jiroskopX)  # Jiroskop X degeri
        packet[50:54] = float_to_bytes(self.dataPacket.jiroskopY)  # Jiroskop Y degeri
        packet[54:58] = float_to_bytes(self.dataPacket.jiroskopZ)  # Jiroskop Z degeri
        packet[58:62] = float_to_bytes(self.dataPacket.ivmeX)  # Ivme X degeri
        packet[62:66] = float_to_bytes(self.dataPacket.ivmeY)  # Ivme Y degeri
        packet[66:70] = float_to_bytes(self.dataPacket.ivmeZ)  # Ivme Z degeri
        packet[70:74] = float_to_bytes(self.dataPacket.aci)  # Aci degeri
        packet[74] = int(self.dataPacket.durum)  # Durum bilgisi
        packet[75] = calculate_checksum(packet)  # Checksum
        packet[76:78] = b'\x0D\x0A'  # Sabit
        self.dataPacket.checksum = packet[75]
        return packet

    @Slot()
    def start_transfer(self):
        reading_port = self.data_reading_device.currentText().split(" ")[0]
        sending_port = self.data_sending_device.currentText().split(" ")[0]
        baudrate_reading = int(self.baudrate_reading.currentText())
        baudrate_sending = int(self.baudrate_sending.currentText())

        try:
            if self.serial_reading:
                self.serial_reading.close()
            if self.serial_sending:
                self.serial_sending.close()
            if (reading_port != "-1") & (sending_port != "-1"):
                self.serial_reading = serial.Serial(reading_port, baudrate_reading)
                self.serial_sending = serial.Serial(sending_port, baudrate_sending)
                self.transfer_thread = threading.Thread(target=self.transfer_data)
                self.transfer_thread.start()
        except Exception as e:
            QMessageBox.critical(self, "Connection Error", f"Failed to connect: {str(e)}")

    def transfer_data(self):
        while self.serial_reading.is_open:
            if self.serial_reading.in_waiting:
                try:
                    # ! Warning: You have to edit this part according to your data packet string
                    packet = self.serial_reading.readline().decode("utf-8").strip().split(",")
                    self.dataPacket.assign_values(packet)
                    if self.serial_sending.is_open:
                        packet = self.construct_send_packet()
                        self.data_packet_signal.emit(self.dataPacket)
                        self.serial_sending.write(packet)
                except:
                    pass            
    def stop_transfer(self):
        if self.serial_reading:
            self.serial_reading.close()
        if self.serial_sending:
            self.serial_sending.close()
        if hasattr(self, 'transfer_thread') and self.transfer_thread.is_alive():
            self.transfer_thread.join()
        print("Serial communication closed.")

    def closeEvent(self, event):
        self.stop_transfer()
        event.accept()
        QApplication.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = SerialWidget()
    widget.show()
    sys.exit(app.exec())