#SQLITE DB INITIAL STRUCTURE

import sqlite3
import time
import os

DB_PATH = "janitor.db"

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY,
            path TEXT UNIQUE,
            name TEXT,
            extension TEXT,
            size INTEGER,
            last_access REAL,
            last_modified REAL,
            folder TEXT,
            last_scanned REAL
        )
        """)
        
        self.conn.commit()

    #CLEAR BEFORE NEW SCAN
    def clear_files(self):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM files')
        self.conn.commit()

    #INSERT || UPDATE RECORD
    def upsert_file(self, info):
        cursor = self.conn.cursor()

        cursor.execute("""
        INSERT INTO files (path, name, extension, size, last_access, last_modified, folder, last_scanned)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(path) DO UPDATE SET
            name = excluded.name,
            extension = excluded.extension,
            size = excluded.size,
            last_access = excluded.last_access,
            last_modified = excluded.last_modified,
            folder = excluded.folder,
            last_scanned = excluded.last_scanned
        """, (
            info["path"],
            info["name"],
            info["extension"],
            info["size"],
            info["last_access"],
            info["last_modified"],
            info["folder"],
            time.time()
        ))

        self.conn.commit()

        #RETRIEVE ALL
    def get_all_files(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM files ORDER BY name ASC")
        return cursor.fetchall()
    
        #RETRIEVE BY EXTENSION
    def get_files_by_extensions(self, ext_list):
        cursor = self.conn.cursor()
        placeholders = ",".join(["?"] * len(ext_list))
        query = f"SELECT * FROM files WHERE extension IN ({placeholders}) ORDER BY name ASC"
        cursor.execute(query, ext_list)
        return cursor.fetchall()
    
    def close(self):
        self.conn.close()