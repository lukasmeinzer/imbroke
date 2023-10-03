"""
TODO fürs nächste Mal:
- DB_Konfiguration.toml ebenso erstellen
- Edeka erstmal postponed, klappt mit bs4 nicht, und selenium braucht einen neuen 
Driver
- Aldi_sued deswegen als nächstes
"""

import toml

import Maerkte.Kaufland as Kaufland
import Maerkte.Edeka as Edeka
import Maerkte.AldiSued as AldiSued

config = toml.load('Crawler_Input.toml')


aldiSued_url = config['Aldi_Sued']['url']
AldiSued.AllAldiSued(url = aldiSued_url)

# kaufland_url = config['Kaufland']['url']
# Kaufland.AllKaufland(url = kaufland_url)

