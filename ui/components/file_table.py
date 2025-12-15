from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem
)
from PyQt6.QtCore import Qt

import os
import subprocess



class FileTable(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Name", "Size", "Last Opened", "Last Modified", "Ext", "Path"
        ])

        self.table.setSortingEnabled(True)
        self.table.setSelectionBehavior(self.table.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.open_context_menu)
        self.table.cellDoubleClicked.connect(self.open_file)

        layout.addWidget(self.table)

        self.full_data = []

    def format_timestamp(self, ts):
        import datetime
        return datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M")
    
    #LOAD DATASET
    def load_data(self, rows):
        self.full_data = rows
        self.table.setRowCount(0)

        for row in rows:
            row_index = self.table.rowCount()
            self.table.insertRow(row_index)

            self.table.setItem(row_index, 0, QTableWidgetItem(row["name"]))

            size_item = QTableWidgetItem(self.format_size_gb(row["size"]))
            size_item.setData(Qt.ItemDataRole.UserRole, row["size"])
            self.table.setItem(row_index, 1, size_item)

            last_open = QTableWidgetItem(self.format_timestamp(row["last_access"]))
            last_open.setData(Qt.ItemDataRole.UserRole, row["last_access"])
            self.table.setItem(row_index, 2, last_open)

            last_mod = QTableWidgetItem(self.format_timestamp(row["last_modified"]))
            last_mod.setData(Qt.ItemDataRole.UserRole, row["last_modified"])
            self.table.setItem(row_index, 3, last_mod)

            self.table.setItem(row_index, 4, QTableWidgetItem(row["extension"]))

            self.table.setItem(row_index, 5, QTableWidgetItem(row["path"]))

    #APPLY FILTER
    def apply_filter(self, text):
        text = text.lower()
        self.table.setRowCount(0)

        for row in self.full_data:
            if text and not (
                text in row["name"].lower()
                or text in row["path"].lower()
                or text in row["extension"].lower()
            ):
                continue

            self.load_data([row])

    def open_context_menu(self, position):
        from PyQt6.QtWidgets import QMenu

        index = self.table.indexAt(position)
        if not index.isValid():
            return
        
        row = index.row()
        path_item = self.table.item(row, 5)
        if not path_item:
            return
        
        path = path_item.text()

        menu = QMenu(self)
        open_file_action = menu.addAction("Open File")
        open_location_action = menu.addAction("Open file location")

        action = menu.exec(self.table.viewport().mapToGlobal(position))
        if not action:
            return

        if action == open_file_action():
            os.startfile(path)
        
        elif action == open_location_action:
            subprocess.run(["explorer", "/select,", path])

    #FILTER BY EXTENSION
    def apply_category_filter(self, extensions):
        self.table.setRowCount(0)

        extset = set(extensions)

        for row in self.full_data:
            if row["extension"].lower() not in extset:
                continue

            size = row["size"]
            last_open = self.format_timestamp(row["last_access"])
            last_mod = self.format_timestamp(row["last_modified"])

            row_index = self.table.rowCount()
            self.table.insertRow(row_index)

            values = [
                row["name"],
                str(size),
                last_open,
                last_mod,
                row["extension"],
                row["path"]
            ]

            for col, v in enumerate(values):
                item = QTableWidgetItem(v)
                if col == 1:
                    item.setData(Qt.ItemDataRole.UserRole, row["size"])
                self.table.setItem(row_index, col, item)

    def format_size_gb(self, size_bytes):
        gb = size_bytes / (1024 ** 3)
        return f"{gb:.2f} GB"