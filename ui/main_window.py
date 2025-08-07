from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QSlider, QFileDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
import cv2
from editor.image_editor import ImageEditor
from utils.file_io import open_image_file, save_image_file


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Photo Editor")
        self.image_editor = ImageEditor()
        self.init_ui()

    def init_ui(self):
        self.image_label = QLabel("Open an image to start")
        self.image_label.setAlignment(Qt.AlignCenter)

        self.brightness_slider = self.create_slider(-100, 100, self.update_image)
        self.contrast_slider = self.create_slider(0, 300, self.update_image, 100)
        self.saturation_slider = self.create_slider(0, 300, self.update_image, 100)

        btn_open = QPushButton("Open Image")
        btn_open.clicked.connect(self.open_image)

        btn_rotate = QPushButton("Rotate 90°")
        btn_rotate.clicked.connect(self.rotate_image)

        btn_undo = QPushButton("Undo")
        btn_undo.clicked.connect(self.undo_edit)

        btn_redo = QPushButton("Redo")
        btn_redo.clicked.connect(self.redo_edit)

        btn_crop = QPushButton("Crop Center")
        btn_crop.clicked.connect(self.crop_image)

        btn_save = QPushButton("Export")
        btn_save.clicked.connect(self.save_image)

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
        button_layout.addWidget(btn_undo)
        button_layout.addWidget(btn_redo)
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
        path = open_image_file(self)
        if path:
            self.image_editor.load_image(path)
            self.update_image()

    def update_image(self):
        if self.image_editor.has_image():
            bright = self.brightness_slider.value()
            cont = self.contrast_slider.value() / 100.0
            sat = self.saturation_slider.value() / 100.0
            img = self.image_editor.apply_edits(bright, cont, sat)
            self.display_image(img)

    def display_image(self, img):
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        bytes_per_line = ch * w
        qt_img = QImage(rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.image_label.setPixmap(QPixmap.fromImage(qt_img).scaled(800, 600, Qt.KeepAspectRatio))

    def rotate_image(self):
        self.image_editor.rotate()
        self.update_image()

    def undo_edit(self):
        img = self.image_editor.undo()
        if img is not None:
            self.display_image(img)

    def redo_edit(self):
        img = self.image_editor.redo()
        if img is not None:
            self.display_image(img)

    def crop_image(self):
        self.image_editor.crop_center()
        self.update_image()

    def save_image(self):
        path = save_image_file(self)
        if path:
            self.image_editor.save(path)