import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QLabel, QSlider, QPushButton, QFileDialog, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

class ImageEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mini Lightroom")
        self.image = None
        self.init_ui()

    def init_ui(self):
        self.label = QLabel("No image")
        self.slider_brightness = QSlider(Qt.Horizontal)
        self.slider_brightness.setRange(-100, 100)
        self.slider_brightness.valueChanged.connect(self.update_image)

        self.button_open = QPushButton("Open Image")
        self.button_open.clicked.connect(self.load_image)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.slider_brightness)
        layout.addWidget(self.button_open)
        self.setLayout(layout)

    def load_image(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', '', "Image files (*.jpg *.png)")
        if fname:
            self.image = cv2.imread(fname)
            self.show_image(self.image)

    def update_image(self, value):
        if self.image is not None:
            img = cv2.convertScaleAbs(self.image, alpha=1, beta=value)  # beta = brightness
            self.show_image(img)

    def show_image(self, img):
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.label.setPixmap(QPixmap.fromImage(qt_image).scaled(600, 400, Qt.KeepAspectRatio))

app = QApplication([])
editor = ImageEditor()
editor.show()
app.exec_()