import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QLabel, QSlider, QPushButton, QFileDialog,
    QVBoxLayout, QHBoxLayout, QWidget, QMainWindow, QAction
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage


class PhotoEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Photo Editor")
        self.image = None
        self.original_image = None
        self.init_ui()

    def init_ui(self):
        self.image_label = QLabel("Open an image to start")
        self.image_label.setAlignment(Qt.AlignCenter)

        # Sliders
        self.brightness_slider = self.create_slider(-100, 100, self.update_image)
        self.contrast_slider = self.create_slider(0, 300, self.update_image, 100)
        self.saturation_slider = self.create_slider(0, 300, self.update_image, 100)

        # Buttons
        btn_open = QPushButton("Open Image")
        btn_open.clicked.connect(self.open_image)

        btn_rotate = QPushButton("Rotate 90°")
        btn_rotate.clicked.connect(self.rotate_image)

        btn_crop = QPushButton("Crop Center")
        btn_crop.clicked.connect(self.crop_image)

        btn_save = QPushButton("Export")
        btn_save.clicked.connect(self.save_image)

        # Layout
        slider_layout = QVBoxLayout()
        slider_layout.addWidget(QLabel("Brightness"))
        slider_layout.addWidget(self.brightness_slider)
        slider_layout.addWidget(QLabel("Contrast"))
        slider_layout.addWidget(self.contrast_slider)
        slider_layout.addWidget(QLabel("Saturation"))
        slider_layout.addWidget(self.saturation_slider)

        button_layout = QHBoxLayout()
        button_layout.addWidget(btn_open)
        button_layout.addWidget(btn_rotate)
        button_layout.addWidget(btn_crop)
        button_layout.addWidget(btn_save)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.image_label)
        main_layout.addLayout(slider_layout)
        main_layout.addLayout(button_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def create_slider(self, min_val, max_val, slot, init=0):
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(min_val)
        slider.setMaximum(max_val)
        slider.setValue(init)
        slider.valueChanged.connect(slot)
        return slider

    def open_image(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.jpeg)")
        if fname:
            self.image = cv2.imread(fname)
            self.original_image = self.image.copy()
            self.update_image()

    def update_image(self):
        if self.image is None:
            return

        img = self.original_image.copy()

        # Brightness and contrast
        brightness = self.brightness_slider.value()
        contrast = self.contrast_slider.value() / 100.0
        img = cv2.convertScaleAbs(img, alpha=contrast, beta=brightness)

        # Saturation (convert to HSV)
        saturation = self.saturation_slider.value() / 100.0
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype(np.float32)
        hsv[..., 1] *= saturation
        hsv[..., 1] = np.clip(hsv[..., 1], 0, 255)
        img = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)

        self.display_image(img)
        self.image = img

    def display_image(self, img):
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image).scaled(800, 600, Qt.KeepAspectRatio)
        self.image_label.setPixmap(pixmap)

    def rotate_image(self):
        if self.image is not None:
            self.original_image = cv2.rotate(self.original_image, cv2.ROTATE_90_CLOCKWISE)
            self.update_image()

    def crop_image(self):
        if self.image is not None:
            h, w = self.original_image.shape[:2]
            start_x = w // 4
            start_y = h // 4
            end_x = start_x + w // 2
            end_y = start_y + h // 2
            self.original_image = self.original_image[start_y:end_y, start_x:end_x]
            self.update_image()

    def save_image(self):
        if self.image is not None:
            fname, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "JPEG (*.jpg);;PNG (*.png)")
            if fname:
                cv2.imwrite(fname, self.image)
                print(f"Saved to {fname}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PhotoEditor()
    window.resize(1000, 800)
    window.show()
    sys.exit(app.exec_())