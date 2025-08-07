from PyQt5.QtWidgets import QFileDialog

def open_image_file(parent):
    path, _ = QFileDialog.getOpenFileName(parent, "Open Image", "", "Image Files (*.jpg *.jpeg *.png)")
    return path

def save_image_file(parent):
    path, _ = QFileDialog.getSaveFileName(parent, "Save Image", "", "JPEG Files (*.jpg);;PNG Files (*.png)")
    return path