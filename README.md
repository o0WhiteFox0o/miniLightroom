# miniLightroom

Hi guys
I'm bored with using a complicated program for photo processing.
I'm creating my own Lightroom tool with python programming language.
This is a personal project and I'm trying to finish it as soon as possible.
I'd love to hear any feedback on ideas or anything else

1. install library:
   pip install PyQt5 opencv-python numpy


2. System structure

├── main.py                   # Chạy chương trình
├── ui/
│   └── main_window.py        # Giao diện chính
├── editor/
│   ├── image_editor.py       # Hàm chỉnh sửa ảnh (brightness, contrast,...)
│   └── history.py            # Undo/redo
├── utils/
│   └── file_io.py            # Mở và lưu ảnh
└── assets/
    └── icons/                # Icon UI