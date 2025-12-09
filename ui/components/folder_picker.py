import os
from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QLabel, QPushButton, QFileDialog
)
from PyQt6.QtCore import Qt

class FolderPicker(QWidget):
    def __init__(self):
        super().__init__()

        self.selected_folders = []

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setAcceptDrops(True)

        #LABEL TO SHOW SELECTED FOLDERS
        self.label = QLabel("Drop folder here or click Browse")
        self.label.setStyleSheet("padding: 6px;")
        layout.addWidget(self.label)

        #BROWSE BUTTON
        self.browse_btn = QPushButton("Browse")
        self.browse_btn.clicked.connect(self.open_dialog)
        layout.addWidget(self.browse_btn)

        self.setLayout(layout)

    def open_dialog(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.selected_folders = [folder]
            self.label.setText(folder)

    #DRAG ENTER EVENT
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    #DROP EVENT
    def dropEvent(self, event):
        urls = event.mimeData().urls()
        folders = []

        for url in urls:
            path = url.toLocalFile()
            if os.path.isdir(path):
                folders.append(path)

        if folders:
            self.selected_folders = folders
            self.label.setText(" | ".join(folders))
            event.acceptProposedAction()
