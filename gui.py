import sqlite3  # Importeer de SQLite3-module voor database-interactie
import tkinter as tk  # Importeer de Tkinter-module en geef deze de alias 'tk'
from tkinter import ttk  # Importeer de ttk-submodule van Tkinter voor theming van widgets
from tkinter import filedialog  # Importeer de filedialog-submodule van Tkinter voor bestandskiezers
import os  # Importeer de os-module voor bestandsbewerkingen
import platform  # Importeer de platform-module voor informatie over het besturingssysteem
from database import create_database, scan_directory  # Importeer de functies create_database en scan_directory uit een extern bestand genaamd 'database'

def scan_and_store(directory_entry, drive_name_entry, result_label):
    # Definieer de functie scan_and_store met parameters directory_entry, drive_name_entry en result_label
    directory = directory_entry.get()  # Haal de ingevoerde map op uit het directory_entry-widget
    drive_name = drive_name_entry.get()  # Haal de ingevoerde schijfnaam op uit het drive_name_entry-widget

    if not os.path.isdir(directory):  # Controleer of het opgegeven pad een geldige map is
        result_label.config(text="Ongeldig pad opgegeven.")  # Configureer het result_label-widget met een foutmelding
        return  # Stop de functie als het pad ongeldig is

    db_path = 'file_database.db'  # Definieer het pad naar de SQLite-database
    connection = sqlite3.connect(db_path)  # Maak verbinding met de SQLite-database
    create_database(connection)  # Maak de database aan als deze nog niet bestaat
    scan_directory(directory, drive_name, connection)  # Scan de geselecteerde mapstructuur en sla deze op in de database
    result_label.config(text="Mapstructuur succesvol gescand en opgeslagen in de database.")  # Configureer het result_label-widget met een succesbericht

def choose_directory(directory_entry, parent_window):
    # Definieer de functie choose_directory met parameters directory_entry en parent_window
    if detect_os() == 'macOS':  # Controleer of het besturingssysteem macOS is
        directory = filedialog.askdirectory(parent=parent_window, title='Kies map')  # Gebruik de juiste methode voor macOS om een map te kiezen
    else:
        directory = filedialog.askdirectory()  # Gebruik de standaardmethode om een map te kiezen voor andere besturingssystemen
        
    directory_entry.delete(0, tk.END)  # Wis de huidige inhoud van het directory_entry-widget
    directory_entry.insert(0, directory)  # Voeg het geselecteerde map pad toe aan het directory_entry-widget

def create_ui():
    # Definieer de functie create_ui om de GUI te maken
    root = tk.Tk()  # Maak een nieuw hoofdvenster (Tkinter root-widget)
    root.title("BESTANDEN SCANNER")  # Geef het hoofdvenster een titel

    directory_label = ttk.Label(root, text="Map om te scannen:")  # Maak een label-widget met de tekst "Map om te scannen:"
    directory_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)  # Plaats het label op rij 1, kolom 0 met uitlijning naar het westen en padding

    directory_entry = ttk.Entry(root, width=40)  # Maak een invoerveld-widget met een breedte van 40 tekens
    directory_entry.grid(row=1, column=1, padx=10, pady=5)  # Plaats het invoerveld op rij 1, kolom 1 met padding

    choose_button = ttk.Button(root, text="Kies map", command=lambda: choose_directory(directory_entry, root))  # Maak een knop-widget met de tekst "Kies map" en wijs de functie choose_directory toe aan de knop
    choose_button.grid(row=1, column=2, padx=5, pady=5)  # Plaats de knop op rij 1, kolom 2 met padding

    drive_name_label = ttk.Label(root, text="Naam/nummer van schijf:")  # Maak een label-widget met de tekst "Naam/nummer van schijf:"
    drive_name_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)  # Plaats het label op rij 2, kolom 0 met uitlijning naar het westen en padding

    drive_name_entry = ttk.Entry(root, width=40)  # Maak een invoerveld-widget voor de schijfnaam met een breedte van 40 tekens
    drive_name_entry.grid(row=2, column=1, padx=10, pady=5)  # Plaats het invoerveld op rij 2, kolom 1 met padding

    scan_button = ttk.Button(root, text="Scan en opslaan", command=lambda: scan_and_store(directory_entry, drive_name_entry, result_label))  # Maak een knop-widget met de tekst "Scan en opslaan" en wijs de functie scan_and_store toe aan de knop
    scan_button.grid(row=3, column=1, pady=10)  # Plaats de knop op rij 3, kolom 1 met padding

    result_label = ttk.Label(root, text="")  # Maak een label-widget voor het resultaat
    result_label.grid(row=4, column=0, columnspan=3, padx=10, pady=5)  # Plaats het resultaatlabel op rij 4, kolom 0 en strek zich uit over drie kolommen met padding

    root.mainloop()  # Start de GUI-lus om het hoofdvenster weer te geven en gebruikersinteractie mogelijk te maken

def detect_os():
    # Definieer de functie detect_os om het besturingssysteem te detecteren
    if platform.system() == 'Windows':  # Controleer of het besturingssysteem Windows is
        return 'Windows'  # Retourneer 'Windows' als het besturingssysteem Windows is
    elif platform.system() == 'Darwin':  # Controleer of het besturingssysteem macOS is
        return 'macOS'  # Retourneer 'macOS' als het besturingssysteem macOS is
    else:
        return 'Unknown'  # Retourneer 'Unknown' als het besturingssysteem niet wordt herkend

create_ui()  # Roep de create_ui-functie aan om de GUI te maken en de applicatie uit te voeren
