from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout

class AudioTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Audio files will appear here"))
        self.setLayout(layout)