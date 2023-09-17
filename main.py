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

url = 'https://filiale.kaufland.de/angebote/aktuelle-woche'

KauflandConnection = Database.KauflandDB()

soup = Kaufland.lade_seite(url, include=['soup'])[0]
# Kaufland.keks_klicker(driver)

meta_info = Kaufland.MetaInfo(soup)
Database.Hochladen(data=meta_info, con=KauflandConnection, name='metainfo')

kategorien = Kaufland.Kategorien(soup)
kategorien_urls = Kaufland.Kategorien_URLs(kategorien, url)

angebote_je_kategorie_urls = Kaufland.Produkt_URLs(kategorien_urls)
angebote = Kaufland.Crawler(angebote_je_kategorie_urls)
Database.Hochladen(data=angebote, con=KauflandConnection, name='angebote')