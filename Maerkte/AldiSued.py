from bs4 import BeautifulSoup
import pandas as pd

import Database
import Utils

def AllAldiSued(url: str):
    
    AldiSuedConnection = Database.AldiSuedDB()
    
    soup = Utils.lade_seite(url, include=['soup'])[0]

    meta_info = MetaInfo(soup)
    Database.Hochladen(data=meta_info, con=AldiSuedConnection, name='metainfo')
    
    angebote_urls = Produkt_URLs(meta_info)
    
    
def MetaInfo(soup):
    
    meta_info = {}
    
    aktuelle_woche = soup.find('h2', 'trenner')
    if aktuelle_woche:
        aktuelle_woche = aktuelle_woche.text.strip()
        meta_info['aktuelle Woche'] = aktuelle_woche
        
    startseite_elements = soup.find_all('a','item-noshadow')
    
    aldiSued_prefix = 'https://www.aldi-sued.de/'
    for e in startseite_elements:
        info_text = e.text.strip()
        url = e['href']
        url = aldiSued_prefix + url
        meta_info[info_text] = url
    
    
    return meta_info
    
    
def Produkt_URLs(urls):
    for key, url in urls.items():
        if key.startswith('aktuelle Woche'):
            continue
        soup = Utils.lade_seite(url, include=['soup'])[0]
