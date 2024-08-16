import sys
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg

class ThreeDimensionalXyzWidget(QWidget):
    def __init__(self, name="Default"):
        super().__init__()
        self.subWidget = QWidget()
        main_layout = QVBoxLayout()
        self.subWidget.setLayout(main_layout)

        self.subWidgetLayout = QVBoxLayout()
        self.subWidgetLayout.addWidget(self.subWidget)
        self.setLayout(self.subWidgetLayout)

        self.label_layout = QHBoxLayout()

        # Create a Matplotlib figure and axes for 3D plot
        self.figure = plt.Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.ax = self.figure.add_subplot(111, projection='3d')
        self.ax.view_init(elev=20, azim=45)
        self.figure.patch.set_facecolor('#201702')
        self.ax.set_facecolor('#201702')

        # Create and configure the name label
        self.name_label = QLabel(f"{name}")
        self.name_label.setStyleSheet("background-color: #fdb513; font-size: 20px; font-weight: bold; font-family: EncodeSans; color: #201702;")
        self.name_label.setAlignment(Qt.AlignCenter)
        self.name_label.setFixedHeight(40)  # Set a fixed height for the name label

        # Create a Matplotlib figure and axes for line plot
        self.line_figure, self.line_ax = plt.subplots()
        self.line_canvas = FigureCanvasQTAgg(self.line_figure)
        self.line_ax.spines['top'].set_edgecolor('#fdb513')
        self.line_ax.spines['right'].set_edgecolor('#fdb513')
        self.line_ax.spines['left'].set_edgecolor('#fdb513')
        self.line_ax.spines['bottom'].set_edgecolor('#fdb513')
        self.line_ax.tick_params(axis='x', colors='#fdb513')
        self.line_ax.tick_params(axis='y', colors='#fdb513')
        self.line_ax.grid(True, color='#fdb513', linestyle='-.', linewidth=0.5)
        self.line_figure.patch.set_facecolor('#201702')
        self.line_ax.set_facecolor('#201702')
        self.line_ax.set_ylim(-360, 360)

        # Initialize data for the line plot
        self.time_data = [0]
        self.time = 0
        self.x_data = [0]
        self.y_data = [0]
        self.z_data = [0]

        # Create a horizontal layout for the graphs
        graph_layout = QHBoxLayout()
        graph_layout.addWidget(self.line_canvas, 2)  # Set stretch factor for the line graph
        graph_layout.addWidget(self.canvas, 1)  # Set stretch factor for the 3D graph

        # Add the name label, graph layout, and label layout to the main layout
        main_layout.addWidget(self.name_label)
        main_layout.addLayout(graph_layout)
        main_layout.addLayout(self.label_layout)

        # Initialize data
        self.x_value = 0
        self.y_value = 0
        self.z_value = 0

        # Create labels for x, y, and z
        self.x_label = QLabel("X: 0")
        self.y_label = QLabel("Y: 0")
        self.z_label = QLabel("Z: 0")

        # Set colors for the labels to match the vectors
        self.x_label.setStyleSheet("color: #dd1113; font-size: 20px; font-weight: bold; font-family: EncodeSans;")
        self.y_label.setStyleSheet("color: #5bfd13; font-size: 20px; font-weight: bold; font-family: EncodeSans;")
        self.z_label.setStyleSheet("color: #13d0fd; font-size: 20px; font-weight: bold; font-family: EncodeSans;")

        self.x_label.setAlignment(Qt.AlignCenter)
        self.y_label.setAlignment(Qt.AlignCenter)
        self.z_label.setAlignment(Qt.AlignCenter)

        # Add labels to the horizontal layout
        self.label_layout.addWidget(self.x_label)
        self.label_layout.addWidget(self.y_label)
        self.label_layout.addWidget(self.z_label)

        self.setStyleSheet("background-color: #201702; border: 2px solid #fdb513; border-radius: 5px; padding: 5px;")
        
        self.plot_data()

    def plot_data(self):
        self.ax.clear()
        self.line_ax.clear()

        # Plot the vectors in the 3D graph
        self.ax.quiver(0, 0, 0, self.x_value, self.y_value, self.z_value, color='white', label='Sum Vector', linestyle='--')
        self.ax.quiver(0, 0, 0, self.x_value, 0, 0, color='#dd1113', label='X Vector')
        self.ax.quiver(0, 0, 0, 0, self.y_value, 0, color='#5bfd13', label='Y Vector')
        self.ax.quiver(0, 0, 0, 0, 0, self.z_value, color='#13d0fd', label='Z Vector')

        # Set labels and limits for the 3D plot
        self.ax.set_xlabel('X', color='white', fontsize=12)
        self.ax.set_ylabel('Y', color='white', fontsize=12)
        self.ax.set_zlabel('Z', color='white', fontsize=12)
        self.ax.set_xlim([-360, 360])
        self.ax.set_ylim([-360, 360])
        self.ax.set_zlim([-360, 360])

        # Set the tick and grid colors for the 3D plot
        self.ax.xaxis.set_tick_params(colors='#fdb513')
        self.ax.yaxis.set_tick_params(colors='#fdb513')
        self.ax.zaxis.set_tick_params(colors='#fdb513')
        self.ax.xaxis._axinfo['grid'].update(color='#fdb513', linestyle='-.', linewidth=0.5)
        self.ax.yaxis._axinfo['grid'].update(color='#fdb513', linestyle='-.', linewidth=0.5)
        self.ax.zaxis._axinfo['grid'].update(color='#fdb513', linestyle='-.', linewidth=0.5)
        for axis in [self.ax.xaxis, self.ax.yaxis, self.ax.zaxis]:
            axis.pane.fill = False  # Make the pane transparent
            axis.line.set_color('#fdb513')  # Set the color of the axis lines

        self.canvas.draw()
        
        # Plot the values over time in the line graph
        self.line_ax.plot(self.time_data, self.x_data, color="#dd1113", lw=2, label='X')
        self.line_ax.plot(self.time_data, self.y_data, color="#5bfd13", lw=2, label='Y')
        self.line_ax.plot(self.time_data, self.z_data, color="#13d0fd", lw=2, label='Z')
        
        # Set the same style for the line graph
        self.line_ax.spines['top'].set_edgecolor('#fdb513')
        self.line_ax.spines['right'].set_edgecolor('#fdb513')
        self.line_ax.spines['left'].set_edgecolor('#fdb513')
        self.line_ax.spines['bottom'].set_edgecolor('#fdb513')
        self.line_ax.tick_params(axis='x', colors='#fdb513')
        self.line_ax.tick_params(axis='y', colors='#fdb513')
        self.line_ax.grid(True, color='#fdb513', linestyle='-.', linewidth=0.5)
        self.line_ax.set_ylim([-360, 360])
        
        self.line_canvas.draw()

    def update(self, x, y, z):
        # Update the vector values
        self.x_value = x
        self.y_value = y
        self.z_value = z

        # Update labels with the latest values
        self.x_label.setText(f"X: {self.x_value:.2f}")
        self.y_label.setText(f"Y: {self.y_value:.2f}")
        self.z_label.setText(f"Z: {self.z_value:.2f}")

        # Update the line graph data
        self.time += 1
        self.time_data.append(self.time)
        self.x_data.append(self.x_value)
        self.y_data.append(self.y_value)
        self.z_data.append(self.z_value)

        if len(self.time_data) > 10:
            self.time_data.pop(0)
            self.x_data.pop(0)
            self.y_data.pop(0)
            self.z_data.pop(0)

        self.plot_data()

    def reset(self):
        self.time = -1
        self.time_data = []
        self.x_data = []
        self.y_data = []
        self.z_data = []
        self.plot_data()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = ThreeDimensionalXyzWidget("3D and Line Graph Widget")
    widget.show()
    sys.exit(app.exec())
