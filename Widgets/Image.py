from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
import sys

class ImageDisplay(QMainWindow):
    def __init__(self, image_path: str = "Assets/logo.png"):
        super().__init__()

        self.layout = QGridLayout()
        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

        self.image_label = QLabel()
        self.layout.addWidget(self.image_label, 0, 0, Qt.AlignRight)  # Align to the right

        self.display_image(image_path)

    def display_image(self, image_path: str):
        image = QImage(image_path)
        if not image.isNull():
            square_size = 200
            scaled_image = image.scaled(square_size, square_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            pixmap = QPixmap.fromImage(scaled_image)
            self.image_label.setPixmap(pixmap)
        else:
            self.image_label.setText("Failed to load image")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    image_display_win = ImageDisplay(image_path="Assets/logo.png")
    image_display_win.show()
    sys.exit(app.exec())
