from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
import sys

class Status(QMainWindow):
    def __init__(self, title="Default Message"):
        super().__init__()
        self.title = title
        self.layout = QHBoxLayout()
        self.title += ": "
        self.i = 0
        
        # Create QLabel and apply font
        self.label = QLabel(text=self.title + str(self.i))
        self.label.setStyleSheet("border: 2px solid #fdb513; font-size: 20px; font-family: EncodeSans; background-color: #201702; text-align: center;")
        # Add QLabel to layout and set central widget
        self.layout.addWidget(self.label)
        self.setCentralWidget(self.label)
        self.alert = ""

    def update(self, status_code: int):
        self.label.setText(f"{self.title}{status_code}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Status()
    window.show()
    sys.exit(app.exec())
