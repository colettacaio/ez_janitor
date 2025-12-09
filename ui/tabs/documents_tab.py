from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout

class DocumentsTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Documents will appear here"))
        self.setLayout(layout)