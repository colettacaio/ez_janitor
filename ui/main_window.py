from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QPushButton, QLabel
)
from PyQt6.QtCore import Qt

from ui.components.folder_picker import FolderPicker

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #WINDOW CONFIG
        self.setWindowTitle("EZ Janitor")
        self.resize(640, 480)
        self.setMinimumSize(20, 20)

        #MAIN LAYOUT
        container = QWidget()
        self.setCentralWidget(container)
        outer_layout = QVBoxLayout(container)

        #TOP BAR
        top_bar = QHBoxLayout()
        outer_layout.addLayout(top_bar)

        #SPACER FOR SCAN BUTTON (SOON TO BE A SEARCH BAR)
        top_bar.addStretch()

        #SCAN BUTTON remove stylesheet from here 
        self.scan_button = QPushButton("Scan")
        self.scan_button.setFixedSize(100, 36)
        self.scan_button.setStyleSheet("""
            QPushButton {
                background-color: #004225;
                color: white;
                border-radius: 6px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #005c34;
            }
            QPushButton:pressed {
                background-color: #00361a;
            }
        """)
        top_bar.addWidget(self.scan_button)

        #MAIN CONTENT AREA
        content_layout = QHBoxLayout()
        outer_layout.addLayout(content_layout)

        #SIDEBAR
        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(150)
        self.sidebar.hide()

        for name in ["All Files", "Images", "Videos", "Audio", "Documents"]:
            QListWidgetItem(name, self.sidebar)

        content_layout.addWidget(self.sidebar)

        #CENTER AREA    
        self.center_area = QWidget()
        self.center_layout = QVBoxLayout(self.center_area)
        content_layout.addWidget(self.center_area)

        #BIG DRAGnDROP
        self.folder_picker_large = FolderPicker(large=True)
        self.center_layout.addWidget(self.folder_picker_large)

        #SMOL DRAGnDROP
        self.folder_picker_small = FolderPicker(large=False)
        self.folder_picker_small.hide()
        self.center_layout.addWidget(self.folder_picker_small)

        #SIDEBAR REVEAL
        self.folder_picker_large.on_folder_selected = self.handle_folder_drop
        self.folder_picker_small.on_folder_selected = self.handle_folder_drop

    def handle_folder_drop(self, folders):
        print("Folders:", folders)

        #HIDE BIG DND, SHOW SMOL DND
        self.folder_picker_large.hide()
        self.folder_picker_small.show()

        #SHOW SIDEBAR
        self.sidebar.show()

        #POPULATE "ALLFILES" TABLE HERE