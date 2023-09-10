"""
TODO fürs nächste Mal:
- In DB MetaInfos zu Kaufland erstmal speichern
- Dann Kaufland scrapen und diese Infos in DB speichern 
- Dann alles für Edeka nach dem exakt gleichem Schema machen
- Scraping_Input.toml erstellen und da die ganzen Variablen reinpacken
- DB_Konfiguration.toml ebenso erstellen
"""


import Kaufland
import Database


url = 'https://filiale.kaufland.de/angebote/aktuelle-woche'

KauflandConnection = Database.KauflandDB()

soup, driver = Kaufland.lade_seite(url)
Kaufland.keks_klicker(driver)

meta_info = Kaufland.MetaInfo(soup)
Database.Hochladen(data=meta_info, con=KauflandConnection, name='MetaInfo')

kategorien = Kaufland.Kategorien(soup)
kategorien_urls = Kaufland.Kategorien_URLs(kategorien, url)

Kaufland.Angebote(kategorien_urls)