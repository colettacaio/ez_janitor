import os
from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QFileDialog, QFrame
)
from PyQt6.QtCore import Qt

class FolderPicker(QWidget):
    def __init__(self, large=False):
        super().__init__()

        self.large = large
        self.selected_folders = []
        self.on_folder_selected = None
        
        self.setAcceptDrops(True)

        if self.large:
            self.build_large_ui()
        else:
            self.build_small_ui()

    def build_large_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        frame = QFrame()
        frame_layout = QVBoxLayout(frame)
        frame_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        frame.setFixedSize(500, 250)
        frame.setStyleSheet("""
            QFrame {
                background-color: #2d2d2d;
                border: 2px dashed #555;
                border-radius: 10px;
            }
        """)

        label = QLabel("Drop folders here")
        label.setStyleSheet("font-size: 20px; color: #cccccc;")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        frame_layout.addWidget(label)

        browse_btn = QPushButton("Browse")
        browse_btn.setFixedSize(100, 32)
        browse_btn.clicked.connect(self.open_dialog)
        frame_layout.addWidget(browse_btn)

        layout.addWidget(frame)

    def build_small_ui(self):
        layout = QHBoxLayout(self)
        
        self.label = QLabel("Select folder")
        self.label.setStyleSheet("padding: 6px; font-size 14px;")

        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.open_dialog)

        layout.addWidget(self.label)
        layout.addWidget(browse_btn)

        #BROWSE DIALOG
    def open_dialog(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.selected_folders = [folder]
            if self.large:
                pass
            else:
                self.label.setText(folder)

            if self.on_folder_selected:
                self.on_folder_selected(self.selected_folders)

                #selectedfolderselfselectedfolderselectedfoldersofselectedselfolderselectedself

        #DRAG ENTER
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

        #DROP EVENT
    def dropEvent(self, event):
        urls = event.mimedata().urls()
        folders = []

        for url in urls:
            path = url.toLocalFile()
            if os.path.isdir(path):
                folders.append(path)

        if folders:
            self.selected_folders = folders
            if self.on_folder_selected:
                self.on_folder_selected(folders)

            event.acceptProposedAction()