"""
TODO fürs nächste Mal:
- angebote_dict (Kaufland) schön in DF formatiern und in DB speichern
    - dafür muss die "hochladen" Funktion noch angepasst und verbessert werden 
        (dass nur DFs hochgeladen werden können)
- Scraping_Input.toml erstellen und da die ganzen Variablen reinpacken
- DataBase in eigenen DB Ordner packen und dann jeweils eine DB File für Connection
- Für Apis evtl je Markt eine eigene DB File
- Dann alles für Edeka nach dem exakt gleichem Schema machen
- DB_Konfiguration.toml ebenso erstellen
"""


import Maerkte.Kaufland as Kaufland
import Database


Kaufland.AllKaufland(url='https://filiale.kaufland.de/angebote/aktuelle-woche')