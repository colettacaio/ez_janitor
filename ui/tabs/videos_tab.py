from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout

class VideosTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Videos will appear here"))
        self.setLayout(layout)