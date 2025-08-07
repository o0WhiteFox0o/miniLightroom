import cv2

class HistoryManager:
    def __init__(self):
        self.stack = []
        self.index = -1

    def add(self, image):
        # Lưu một bản sao của ảnh
        img_copy = image.copy()
        if self.index < len(self.stack) - 1:
            self.stack = self.stack[:self.index + 1]  # Bỏ các bước redo sau nếu có
        self.stack.append(img_copy)
        self.index += 1

    def undo(self):
        if self.can_undo():
            self.index -= 1
            return self.stack[self.index]
        return None

    def redo(self):
        if self.can_redo():
            self.index += 1
            return self.stack[self.index]
        return None

    def can_undo(self):
        return self.index > 0

    def can_redo(self):
        return self.index + 1 < len(self.stack)

    def get_current(self):
        if 0 <= self.index < len(self.stack):
            return self.stack[self.index]
        return None

    def reset(self):
        self.stack.clear()
        self.index = -1