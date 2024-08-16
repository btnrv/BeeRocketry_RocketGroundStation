import sys
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg

import matplotlib.pyplot as plt

class RollYawPitchWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.subWidget = QWidget()
        self.subWidget.setStyleSheet("background-color: #201702; border: 2px solid #fdb513; border-radius: 5px; padding: 5px;")

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.subWidget)
        self.setLayout(main_layout)

        sub_layout = QVBoxLayout()
        self.subWidget.setLayout(sub_layout)

        self.title_label = QLabel("Roll,  Yaw,  Pitch")
        self.title_label.setStyleSheet("background-color: #fdb513; font-size: 20px; font-weight: bold; font-family: EncodeSans; color: #201702;")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFixedHeight(40)
        sub_layout.addWidget(self.title_label)

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.ax.spines['top'].set_edgecolor('#fdb513')
        self.ax.spines['right'].set_edgecolor('#fdb513')
        self.ax.spines['left'].set_edgecolor('#fdb513')
        self.ax.spines['bottom'].set_edgecolor('#fdb513')
        self.ax.tick_params(axis='x', colors='#fdb513')
        self.ax.tick_params(axis='y', colors='#fdb513')
        self.ax.grid(True, color='#fdb513', linestyle='-.', linewidth=0.5)
        self.figure.patch.set_facecolor('#201702')
        self.ax.set_facecolor('#201702')
        self.ax.set_ylim(-360, 360)
        sub_layout.addWidget(self.canvas)

        self.roll_data = [0]
        self.yaw_data = [0]
        self.pitch_data = [0]
        self.time_data = [0]
        self.time = 0

        self.r_label = QLabel("Roll: 0")
        self.y_label = QLabel("Yaw: 0")
        self.p_label = QLabel("Pitch: 0")
        self.r_label.setStyleSheet("color: #dd1113; font-size: 20px; font-weight: bold; font-family: EncodeSans;")
        self.y_label.setStyleSheet("color: #5bfd13; font-size: 20px; font-weight: bold; font-family: EncodeSans;")
        self.p_label.setStyleSheet("color: #13d0fd; font-size: 20px; font-weight: bold; font-family: EncodeSans;")
        self.r_label.setAlignment(Qt.AlignCenter)
        self.y_label.setAlignment(Qt.AlignCenter)
        self.p_label.setAlignment(Qt.AlignCenter)

        self.label_layout = QHBoxLayout()
        self.label_layout.addWidget(self.r_label)
        self.label_layout.addWidget(self.y_label)
        self.label_layout.addWidget(self.p_label)
        sub_layout.addLayout(self.label_layout)

        self.plot_data()

    def plot_data(self):
        self.ax.clear()
        self.roll_line, = self.ax.plot(self.time_data, self.roll_data, color="#dd1113", lw=2, label='Roll')
        self.yaw_line, = self.ax.plot(self.time_data, self.yaw_data, color="#5bfd13", lw=2, label='Yaw')
        self.pitch_line, = self.ax.plot(self.time_data, self.pitch_data, color="#13d0fd", lw=2, label='Pitch')

        self.ax.spines['top'].set_edgecolor('#fdb513')
        self.ax.spines['right'].set_edgecolor('#fdb513')
        self.ax.spines['left'].set_edgecolor('#fdb513')
        self.ax.spines['bottom'].set_edgecolor('#fdb513')
        self.ax.tick_params(axis='x', colors='#fdb513')
        self.ax.tick_params(axis='y', colors='#fdb513')
        self.ax.grid(True, color='#fdb513', linestyle='-.', linewidth=0.5)
        self.ax.set_ylim([-360, 360])

        self.canvas.draw()

    def update(self, r, y, p):
        self.roll_data.append(r)
        self.yaw_data.append(y)
        self.pitch_data.append(p)
        self.time += 1
        self.time_data.append(self.time)

        if len(self.time_data) > 10:
            self.roll_data.pop(0)
            self.yaw_data.pop(0)
            self.pitch_data.pop(0)
            self.time_data.pop(0)
        
        self.r_label.setText(f"Roll: {r:.2f}")
        self.y_label.setText(f"Yaw: {y:.2f}")
        self.p_label.setText(f"Pitch: {p:.2f}")

        self.plot_data()

    def reset(self):
        self.roll_data = []
        self.yaw_data = []
        self.pitch_data = []
        self.time_data = []
        self.time = -1
        self.plot_data()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = RollYawPitchWidget()
    widget.show()
    sys.exit(app.exec())
