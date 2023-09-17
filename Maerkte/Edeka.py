
from bs4 import BeautifulSoup

import Database
import Utils

def AllEdeka(url: str):
    
    EdekaConnection = Database.EdekaDB()
    
    soup = Utils.lade_seite(url, include=['soup'])[0]

    meta_info = MetaInfo(soup)


def MetaInfo(soup: BeautifulSoup):
    aktuelle_woche = soup.find_all('span', class_='css-1skty0g')
    if aktuelle_woche:
        aktuelle_woche = aktuelle_woche.text.strip()