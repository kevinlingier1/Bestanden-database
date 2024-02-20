import sqlite3
import os

# Functie om de database aan te maken als deze nog niet bestaat
def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS files (id INTEGER PRIMARY KEY, drive_name TEXT, directory TEXT, file_name TEXT, file_path TEXT)")
    connection.commit()


# Functie om de mapstructuur te scannen en op te slaan in de database
def scan_directory(directory, drive_name, connection):
    cursor = connection.cursor()
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, directory)
            directory_path, file_name = os.path.split(relative_path)
            cursor.execute("INSERT INTO files (drive_name, directory, file_name, file_path) VALUES (?, ?, ?, ?)",
                           (drive_name, directory_path, file_name, file_path))
    connection.commit()