import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import platform
from database import create_database, scan_directory

def scan_and_store(directory_entry, drive_name_entry, result_label):
    directory = directory_entry.get()
    drive_name = drive_name_entry.get()

    if not os.path.isdir(directory):
        result_label.config(text="Ongeldig pad opgegeven.")
        return

    db_path = 'file_database.db'
    connection = sqlite3.connect(db_path)
    create_database(connection)
    scan_directory(directory, drive_name, connection)
    result_label.config(text="Mapstructuur succesvol gescand en opgeslagen in de database.")

def choose_directory(directory_entry):
    if detect_os() == 'macOS':
        directory = filedialog.askdirectory(parent=root, title='Kies map')  # Gebruik de juiste methode voor macOS
    else:
        directory = filedialog.askdirectory()  # Gebruik de standaardmethode voor andere besturingssystemen
        
    directory_entry.delete(0, tk.END)
    directory_entry.insert(0, directory)

def create_ui():
    root = tk.Tk()
    root.title("BESTANDEN SCANNER")

    directory_label = ttk.Label(root, text="Map om te scannen:")
    directory_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)

    directory_entry = ttk.Entry(root, width=40)
    directory_entry.grid(row=1, column=1, padx=10, pady=5)

    choose_button = ttk.Button(root, text="Kies map", command=lambda: choose_directory(directory_entry))
    choose_button.grid(row=1, column=2, padx=5, pady=5)

    drive_name_label = ttk.Label(root, text="Naam/nummer van schijf:")
    drive_name_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)

    drive_name_entry = ttk.Entry(root, width=40)
    drive_name_entry.grid(row=2, column=1, padx=10, pady=5)

    scan_button = ttk.Button(root, text="Scan en opslaan", command=lambda: scan_and_store(directory_entry, drive_name_entry, result_label))
    scan_button.grid(row=3, column=1, pady=10)

    result_label = ttk.Label(root, text="")
    result_label.grid(row=4, column=0, columnspan=3, padx=10, pady=5)

    root.mainloop()

def detect_os():
    if platform.system() == 'Windows':
        return 'Windows'
    elif platform.system() == 'Darwin':
        return 'macOS'
    else:
        return 'Unknown'

create_ui()
