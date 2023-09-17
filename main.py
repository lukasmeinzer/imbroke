"""
TODO fürs nächste Mal:
- DB_Konfiguration.toml ebenso erstellen
- Edeka erstmal postponed, klappt mit bs4 nicht, und selenium braucht einen neuen 
Driver
- 
"""

import toml

import Maerkte.Kaufland as Kaufland
import Maerkte.Edeka as Edeka

config = toml.load('Crawler_Input.toml')


kaufland_url = config['Kaufland']['url']
Kaufland.AllKaufland(kaufland_url)


edeka_url = config['Edeka']['url']
Edeka.AllEdeka(edeka_url)
