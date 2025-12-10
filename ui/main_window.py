from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QProgressBar, QVBoxLayout, QHBoxLayout, QLineEdit, QListWidget, QListWidgetItem, QPushButton, QLabel
)
from PyQt6.QtCore import Qt

from ui.components.folder_picker import FolderPicker
from ui.components.file_table import FileTable

from core.scanner import ScanWorker
from core.db import Database



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.db = Database ()

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

        #SEARCH BAR
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search files...")
        self.search_bar.setFixedWidth(250)
        self.search_bar.textChanged.connect(self.handle_search)
        top_bar.addWidget(self.search_bar)

        #PROGRESS BAR
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedWidth(200)
        self.progress_bar.setVisible(False)
        top_bar.addWidget(self.progress_bar)

        #SPACER
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
        self.scan_button.clicked.connect(self.start_scan)

        #MAIN CONTENT AREA
        content_layout = QHBoxLayout()
        outer_layout.addLayout(content_layout)

        #SIDEBAR
        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(150)
        self.sidebar.hide()
        self.sidebar.currentItemChanged.connect(self.handle_sidebar_change)

        for name in ["All Files", "Images", "Videos", "Audio", "Documents", "Other"]:
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

        #FILE TABLE
        self.file_table = FileTable()
        self.file_table.hide()
        self.center_layout.addWidget(self.file_table)

        #SIDEBAR REVEAL
        self.folder_picker_large.on_folder_selected = self.handle_folder_drop
        self.folder_picker_small.on_folder_selected = self.handle_folder_drop

        
    #FOLDER DROP
    def handle_folder_drop(self, folders):
        print("Selected folders:", folders)

        #HIDE BIG DND, SHOW SMOL DND
        self.folder_picker_large.hide()
        self.folder_picker_small.show()

        #SHOW SIDEBAR
        self.sidebar.show()

        #WILL EVENTUALLY TRIGGER SCANNER THREAD
        self.show_file_table()

    
    #SEARCH BAR LOGIC
    def handle_search (self, text):
        if hasattr(self, "file_table"):
            self.file_table.apply_filter(text)

    #REPLACE DND WITH TABLE AFTER SCAN
    def show_file_table(self):
        self.folder_picker_large.hide()
        self.file_table.show()

    #SCAN METHOD
    def start_scan(self):
        folders = self.folder_picker_large.selected_folders or self.folder_picker_small.selected_folders

        if not folders:
            print("No folders selected.")
            return
        
        #SET UI
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.sidebar.hide()
        self.file_table.hide()

        #SET DB
        self.db.clear_files()

        #SET WORKER
        self.worker = ScanWorker(folders)
        self.worker.progress.connect(self.update_progress)
        self.worker.file_found.connect(self.store_file_metadata)
        self.worker.finished.connect(self.finish_scan)
        self.worker.start()

    #PROGRESS UPDATE
    def update_progress(self, pct):
        self.progress_bar.setValue(pct)

    #STORE FILE IN DB
    def store_file_metadata(self, info):
        self.db.upsert_file(info)

    #SCAN FINISH
    def finish_scan(self):
        self.progress_bar.setVisible(False)

        #LOAD DATA
        rows = self.db.get_all_files()
        self.file_table.load_data(rows)

        #SHOW TABLE
        self.show_file_table()

        #SHOW SIDEBAR
        self.sidebar.show()

        print("Scan complete. Files Loaded :)", len(rows))

    #SIDEBAR FILTERING
    def handle_sidebar_change(self, current, previous):
        if not current:
            return
        
        category = current.text()

        image_exts = ["jpg", "jpeg", "png", "gif", "bmp", "webp", "tiff", "ico"]
        video_exts = ["mp4", "mkv", "avi", "mov", "webm"]
        audio_exts = ["mp3", "wav", "flac", "ogg", "m4a"]
        document_exts = ["pdf", "txt", "docx", "xlsx", "pptx"]

        if category == "All Files":
            rows = self.db.get_all_files()
            self.file_table.load_data(rows)
            return
                     
        if category == "Images":
            exts = image_exts
            rows = self.db.get_files_by_extensions(exts)
            self.file_table.load_data(rows)
            return
        
        if category == "Videos":
            exts = video_exts
            rows = self.db.get_files_by_extensions(exts)
            self.file_table.load_data(rows)
            return
        
        if category == "Audio":
            exts = audio_exts
            rows = self.db.get_files_by_extensions(exts)
            self.file_table.load_data(rows)
            return
        
        if category == "Documents":
            exts = document_exts
            rows = self.db.get_files_by_extensions(exts)
            self.file_table.load_data(rows)
            return
        
        if category == "Other":
            all_rows = self.db.get_all_files()
            known = set(image_exts + video_exts + audio_exts + document_exts)
            other_rows = [r for r in all_rows if r["extension"] not in known]
            self.file_table.load_data(other_rows)
            return
        

      