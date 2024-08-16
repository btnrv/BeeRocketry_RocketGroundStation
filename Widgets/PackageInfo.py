import sys
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
import matplotlib.pyplot as plt

class PackageInfo(QWidget):
    def __init__(self):
        super().__init__()

        self.subWidget = QWidget()
        self.subWidget.setStyleSheet("background-color: #201702; border: 2px solid #fdb513; border-radius: 5px; padding: 5px;")

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.subWidget)
        self.setLayout(main_layout)

        sub_layout = QVBoxLayout()
        self.subWidget.setLayout(sub_layout)

        # Title label
        self.title_label = QLabel("Moisture and Temperature")
        self.title_label.setStyleSheet("background-color: #fdb513; font-size: 20px; font-weight: bold; font-family: EncodeSans; color: #201702;")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFixedHeight(40)
        sub_layout.addWidget(self.title_label)

        # Create two subplots for moisture and temperature
        self.figure, (self.moisture_ax, self.temperature_ax) = plt.subplots(1, 2, figsize=(10, 4))
        self.canvas = FigureCanvasQTAgg(self.figure)

        # Set background color for the figure and axes
        self.figure.patch.set_facecolor('#201702')
        self.moisture_ax.set_facecolor('#201702')
        self.temperature_ax.set_facecolor('#201702')

        # Customize moisture plot
        self.moisture_ax.spines['top'].set_edgecolor('#fdb513')
        self.moisture_ax.spines['right'].set_edgecolor('#fdb513')
        self.moisture_ax.spines['left'].set_edgecolor('#fdb513')
        self.moisture_ax.spines['bottom'].set_edgecolor('#fdb513')
        self.moisture_ax.tick_params(axis='x', colors='#fdb513')
        self.moisture_ax.tick_params(axis='y', colors='#fdb513')
        self.moisture_ax.grid(True, color='#fdb513', linestyle='-.', linewidth=0.5)
        self.moisture_ax.set_ylim(0, 100)
        self.moisture_ax.set_xlim(0, 10)

        # Customize temperature plot
        self.temperature_ax.spines['top'].set_edgecolor('#fdb513')
        self.temperature_ax.spines['right'].set_edgecolor('#fdb513')
        self.temperature_ax.spines['left'].set_edgecolor('#fdb513')
        self.temperature_ax.spines['bottom'].set_edgecolor('#fdb513')
        self.temperature_ax.tick_params(axis='x', colors='#fdb513')
        self.temperature_ax.tick_params(axis='y', colors='#fdb513')
        self.temperature_ax.grid(True, color='#fdb513', linestyle='-.', linewidth=0.5)
        self.temperature_ax.set_ylim(-20, 150)
        self.temperature_ax.set_xlim(0, 10)

        # Add the canvas to the layout
        sub_layout.addWidget(self.canvas)

        # Initialize data
        self.moisture_data = [0]
        self.temperature_data = [0]
        self.time_data = [0]
        self.time = 0

        # Data labels for moisture and temperature
        self.moisture_label = QLabel("Moisture: 0%")
        self.temperature_label = QLabel("Temperature: 0°C")
        self.moisture_label.setStyleSheet("color: #13d0fd; font-size: 20px; font-weight: bold; font-family: EncodeSans;")
        self.temperature_label.setStyleSheet("color: #dd1113; font-size: 20px; font-weight: bold; font-family: EncodeSans;")
        self.moisture_label.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)

        # Create a horizontal layout for the labels
        label_layout = QHBoxLayout()
        label_layout.addWidget(self.moisture_label)
        label_layout.addWidget(self.temperature_label)

        # Add the label layout to the sub-layout
        sub_layout.addLayout(label_layout)

        self.plot_data()

    def plot_data(self):
        self.moisture_ax.clear()
        self.temperature_ax.clear()

        # Plot the moisture data
        self.moisture_ax.plot(self.time_data, self.moisture_data, color="#13d0fd", lw=2)

        # Plot the temperature data
        self.temperature_ax.plot(self.time_data, self.temperature_data, color="#dd1113", lw=2)

        # Customize moisture plot
        self.moisture_ax.spines['top'].set_edgecolor('#fdb513')
        self.moisture_ax.spines['right'].set_edgecolor('#fdb513')
        self.moisture_ax.spines['left'].set_edgecolor('#fdb513')
        self.moisture_ax.spines['bottom'].set_edgecolor('#fdb513')
        self.moisture_ax.tick_params(axis='x', colors='#fdb513')
        self.moisture_ax.tick_params(axis='y', colors='#fdb513')
        self.moisture_ax.grid(True, color='#fdb513', linestyle='-.', linewidth=0.5)
        self.moisture_ax.set_ylim(0, 100)

        # Customize temperature plot
        self.temperature_ax.spines['top'].set_edgecolor('#fdb513')
        self.temperature_ax.spines['right'].set_edgecolor('#fdb513')
        self.temperature_ax.spines['left'].set_edgecolor('#fdb513')
        self.temperature_ax.spines['bottom'].set_edgecolor('#fdb513')
        self.temperature_ax.tick_params(axis='x', colors='#fdb513')
        self.temperature_ax.tick_params(axis='y', colors='#fdb513')
        self.temperature_ax.grid(True, color='#fdb513', linestyle='-.', linewidth=0.5)
        self.temperature_ax.set_ylim(-20, 150)

        # Draw the canvas
        self.canvas.draw()

    def update(self, moisture, temperature):
        self.moisture_data.append(moisture)
        self.temperature_data.append(temperature)
        self.time += 1
        self.time_data.append(self.time)

        if len(self.time_data) > 10:
            self.moisture_data.pop(0)
            self.temperature_data.pop(0)
            self.time_data.pop(0)
            
        self.moisture_label.setText(f"Moisture: {moisture:.2f}%")
        self.temperature_label.setText(f"Temperature: {temperature:.2f}°C")

        self.plot_data()

    def reset(self):
        self.moisture_data = []
        self.temperature_data = []
        self.time_data = []
        self.time = -1
        self.plot_data()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = PackageInfo()
    widget.show()
    sys.exit(app.exec())
