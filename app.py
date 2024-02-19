import os
import sqlite3

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

# Functie om de database aan te maken als deze nog niet bestaat
def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS files (id INTEGER PRIMARY KEY, drive_name TEXT, directory TEXT, file_name TEXT, file_path TEXT)")
    connection.commit()

# Hoofdprogramma om de mapstructuur te scannen en op te slaan in de database
def main():
    directory = input("Geef het pad naar de map op die je wilt scannen: ")
    if not os.path.isdir(directory):
        print("Ongeldig pad opgegeven.")
        return

    drive_name = input("Geef een naam of nummer voor deze schijf: ")

    db_path = 'file_database.db'
    connection = sqlite3.connect(db_path)
    create_database(connection)
    scan_directory(directory, drive_name, connection)
    print("Mapstructuur succesvol gescand en opgeslagen in de database.")

if __name__ == "__main__":
    main()