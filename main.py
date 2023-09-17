"""
TODO fürs nächste Mal:
- DataBase in eigenen DB Ordner packen und dann jeweils eine DB File für Connection
- Für Apis evtl je Markt eine eigene DB File
- Dann alles für Edeka nach dem exakt gleichem Schema machen
- DB_Konfiguration.toml ebenso erstellen
"""

import toml

import Maerkte.Kaufland as Kaufland


config = toml.load('Crawler_Input.toml')

kaufland_url = config['Kaufland']['url']
Kaufland.AllKaufland(kaufland_url)