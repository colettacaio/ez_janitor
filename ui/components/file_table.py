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
        self.apply_filter("")

    #APPLY FILTER
    def apply_filter(self, text):
        text = text.lower()
        self.table.setRowCount(0)

        for row in self.full_data:
            name = row["name"]
            path = row["path"]
            ext = row["extension"]

            match = (
                text in name.lower() or
                text in path.lower() or
                text in ext.lower()
            )

            if text and not match:
                continue

            size = row["size"]
            last_open = self.format_timestamp(row["last_access"])
            last_mod = self.format_timestamp(row["last_modified"])
            ext_display = ext

            row_index = self.table.rowCount()
            self.table.insertRow(row_index)

            values = [
                name,
                str(size),
                last_open,
                last_mod,
                ext_display,
                path
            ]

            for col, v in enumerate(values):
                item = QTableWidgetItem(v)
                if col == 1:
                    item.setData(Qt.ItemDataRole.UserRole, size)
                self.table.setItem(row_index, col, item)

    def open_context_menu(self, position):
        from PyQt6.QtWidgets import QMenu

        menu = menu()
        open_file_action = menu.addAction("Open file")
        open_location_action = menu.addAction("Open file location")

        action = menu.exec(self.table.viewport().mapToGlobal(position))
        if not action:
            return
        
        selected = self.table.selectedItems()
        if not selected:
            return
        
        row = selected[0].row()
        path = self.table.item(row, 5).text()

        if action == open_file_action:
            os.startfile(path)

        if action == open_location_action:
            subprocess.run(["explorer", "/select", path])

    def open_file(self, row, column):
        path = self.table.item(row, 5).text()
        try:
            os.startfile(path)
        except Exception as e:
            print("Failed to open file:", e)

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