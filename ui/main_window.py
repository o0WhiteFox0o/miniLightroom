from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QSlider, QFileDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage, QColor, QPainter, QPen
import cv2
import numpy as np
from editor.image_editor import ImageEditor
from utils.file_io import open_image_file, save_image_file


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Photo Editor")
        self.image_editor = ImageEditor()
        self.init_ui()
        self.brush_enabled = False
        self.brush_color = QColor("red")
        self.brush_size = 10

        self.last_point = None  # To track last position when drawing
        self.drawing_layer = None  # Layer for drawing

    def init_ui(self):
        self.image_label = QLabel("Open an image to start")
        self.image_label.setAlignment(Qt.AlignCenter)

        self.brightness_slider = self.create_slider(-100, 100, self.update_image)
        self.contrast_slider = self.create_slider(0, 300, self.update_image, 100)
        self.saturation_slider = self.create_slider(0, 300, self.update_image, 100)

        btn_open = QPushButton("Open Image")
        btn_open.clicked.connect(self.open_image)

        brush_btn = QPushButton("Brush")
        brush_btn.clicked.connect(self.toggle_brush)

        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.sync_pixmap_to_image)


        btn_rotate = QPushButton("Rotate 90°")
        btn_rotate.clicked.connect(self.rotate_image)

        btn_undo = QPushButton("Undo")
        btn_undo.clicked.connect(self.undo_edit)

        btn_redo = QPushButton("Redo")
        btn_redo.clicked.connect(self.redo_edit)

        btn_crop = QPushButton("Crop")
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
        button_layout.addWidget(brush_btn)
        button_layout.addWidget(save_btn)
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

    def sync_pixmap_to_image(self):
        pixmap = self.image_label.pixmap()
        if pixmap:
            qimg = pixmap.toImage().convertToFormat(QImage.Format_BGR888)
            width, height = qimg.width(), qimg.height()
            ptr = qimg.bits()
            ptr.setsize(qimg.byteCount())
            arr = np.array(ptr, dtype=np.uint8).reshape((height, width, 3))
            if hasattr(self.image_editor, "set_image"):
                self.image_editor.set_image(arr.copy())
            else:
                print("ImageEditor chưa có hàm set_image")


    def toggle_brush(self):
        self.brush_enabled = not self.brush_enabled
        print("Brush:", "ON" if self.brush_enabled else "OFF")

    def mousePressEvent(self, event):
        if self.brush_enabled and event.button() == Qt.LeftButton:
            self.last_point = event.pos()

    def mouseMoveEvent(self, event):
        if self.brush_enabled and self.last_point:
            painter = QPainter(self.image_label.pixmap())
            pen = QPen(self.brush_color, self.brush_size, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            painter.setPen(pen)
            painter.drawLine(self.last_point, event.pos())
            painter.end()

            self.last_point = event.pos()
            self.image_label.update()



    def mouseReleaseEvent(self, event):
        if self.brush_enabled and event.button() == Qt.LeftButton:
            self.last_point = None

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