from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg

class Altitude(QWidget):
    def __init__(self, name: str, color="#00ffff"):
        super().__init__()
        self.name = name
        self.color = color

        # SubWidget system
        self.subWidget = QWidget()
        main_layout = QVBoxLayout()
        self.subWidget.setLayout(main_layout)

        self.subWidgetLayout = QVBoxLayout()
        self.subWidgetLayout.addWidget(self.subWidget)
        self.setLayout(self.subWidgetLayout)

        # Create the altitude label with the name
        self.altitude_label = QLabel(f"{name} Altitude")
        self.altitude_label.setStyleSheet(
            "background-color: #fdb513; font-size: 20px; font-weight: bold; font-family: EncodeSans; color: #201702;")
        self.altitude_label.setAlignment(Qt.AlignCenter)
        self.altitude_label.setFixedHeight(40)

        # Create a Matplotlib figure and axes for the altitude plot
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

        # Initialize the altitude data
        self.altitude_line, = self.ax.plot([], [], color=color, lw=2, label=name)
        self.ax.legend(loc='upper left', edgecolor='white')
        self.altitude_data = []
        self.time_range = []
        self.time = 0

        # Add a red dashed horizontal line at y=4500
        self.ax.axhline(y=4500, color='red', linestyle='--', linewidth=2)

        # Create the current value label
        self.currentValueLabel = QLabel("0m")
        self.currentValueLabel.setStyleSheet(
            f"color: {color}; font-size: 20px; font-weight: bold; font-family: EncodeSans; background-color: #201702;")
        self.currentValueLabel.setAlignment(Qt.AlignCenter)

        # Add widgets to the main layout
        main_layout.addWidget(self.altitude_label)
        main_layout.addWidget(self.canvas)
        main_layout.addWidget(self.currentValueLabel)

        # Set the main widget style
        self.setStyleSheet("background-color: #201702; border: 2px solid #fdb513; border-radius: 5px; padding: 5px;")

    def update(self, altitudeData: float):
        self.time += 1
        self.altitude_data.append(altitudeData)
        self.time_range.append(self.time)

        # Update the line data
        self.altitude_line.set_data(self.time_range, self.altitude_data)

        # Update x and y-axis limits
        self.ax.set_xlim(min(self.time_range), max(self.time_range))
        self.ax.set_ylim(min(-30, min(self.altitude_data) - 10), max(90, max(self.altitude_data) + 10))

        self.currentValueLabel.setText(f"{altitudeData:.2f}m")
        # Redraw the canvas
        self.canvas.draw()

    def reset(self):
        self.altitude_data = []
        self.time_range = []
        self.time = -1
        self.altitude_line.set_data(self.time_range, self.altitude_data)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Altitude(name="Default", color="#00ffff")
    widget.show()
    sys.exit(app.exec())
