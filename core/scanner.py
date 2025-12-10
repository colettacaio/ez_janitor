#FILE SCANNING THREADED LOGIC

import os
import time
from PyQt6.QtCore import QThread, pyqtSignal



class ScanWorker(QThread):
    progress = pyqtSignal(int)
    file_found = pyqtSignal(dict)
    finished = pyqtSignal()

    def __init__(self, folders):
        super().__init__()
        self.folders = folders
        self.running = True

    def run(self):
        all_files = []

        total = 0
        for folder in self.folders:
            for root, dirs, files in os.walk(folder):
                total += len(files)

        if total == 0:
            self.finished.emit()
            return
        
        processed = 0


        for folder in self.folders:
            for root, dirs, files in os.walk(folder):
                for name in files:
                    if not self.running:
                        return
                    
                    path = os.path.join(root, name)

                    try:
                        stats = os.stat(path)
                        file_info = {
                            "name": name,
                            "path": path,
                            "extension":os.path.splitext(name)[1].lower().replace('.', ''),
                            "size": stats.st_size,
                            "last_access": stats.st_atime,
                            "last_modified": stats.st_mtime,
                            "folder": folder,
                        }
                        self.file_found.emit(file_info)
                    except:
                        pass #SKIP UNREADABLE

                    processed += 1
                    pct = int((processed / total) * 100)
                    self.progress.emit(pct)

        self.finished.emit()

    def stop(self):
        self.running = False



                        