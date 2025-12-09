from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QTabWidget, QPushButton, QLabel
)
from PyQt6.QtCore import Qt

from ui.components.folder_picker import FolderPicker
from ui.tabs.documents_tab import DocumentsTab
from ui.tabs.images_tab import ImagesTab
from ui.tabs.videos_tab import VideosTab
from ui.tabs.audio_tab import AudioTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("EZ Janitor")
        self.setMinimumSize(1100, 700)

        layout = QVBoxLayout()
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        #FOLDER PICKER
        self.folder_picker = FolderPicker()
        layout.addWidget(self.folder_picker)

        #SCAN BUTTON
        self.scan_button = QPushButton("Scan")
        self.scan_button.setFixedHeight(40)
        layout.addWidget(self.scan_button)

        #TABS
        self.tabs = QTabWidget()
        self.tabs.addTab(ImagesTab(), "Images")
        self.tabs.addTab(VideosTab(), "Videos")
        self.tabs.addTab(AudioTab(), "Audio")
        self.tabs.addTab(DocumentsTab(), "Documents")

        layout.addWidget(self.tabs)

    def run_scan(self):
        print("Selected folders:", self.folder_picker.selected_folders)