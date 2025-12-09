from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout

class ImagesTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Images will appear here"))
        self.setLayout(layout)