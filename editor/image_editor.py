import cv2
import numpy as np
from .history import HistoryManager

class ImageEditor:
    def __init__(self):
        self.original = None
        self.current = None
        self.history = HistoryManager()

    def load_image(self, path):
        self.original = cv2.imread(path)
        self.history.reset()
        self.history.add(self.original)
        self.current = self.original.copy()

    def has_image(self):
        return self.original is not None

    def apply_edits(self, brightness, contrast, saturation):
        img = self.original.copy()
        img = cv2.convertScaleAbs(img, alpha=contrast, beta=brightness)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype(np.float32)
        hsv[..., 1] *= saturation
        hsv[..., 1] = np.clip(hsv[..., 1], 0, 255)
        self.current = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
        return self.current

    def rotate(self):
        if self.has_image():
            self.original = self.history.get_current()
            rotated  = cv2.rotate(self.original, cv2.ROTATE_90_CLOCKWISE)
            self.history.add(rotated)
            self.current = rotated

    def crop_center(self):
        if self.has_image():
            img = self.history.get_current()
            h, w = img.shape[:2]
            x, y = w // 4, h // 4
            cropped = img[y:y + h // 2, x:x + w // 2]
            self.history.add(cropped)
            self.current = cropped

    def undo(self):
        img = self.history.undo()
        if img is not None:
            self.current = img
        return img

    def redo(self):
        img = self.history.redo()
        if img is not None:
            self.current = img
        return img

    def save(self, path):
        if self.current is not None:
            cv2.imwrite(path, self.current)