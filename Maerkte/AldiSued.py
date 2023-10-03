from bs4 import BeautifulSoup
import pandas as pd
from collections import defaultdict
import re

import Database
import Utils

def AllAldiSued(url: str):
    
    AldiSuedConnection = Database.AldiSuedDB()
    
    soup = Utils.lade_seite(url, include=['soup'])[0]

    meta_info = MetaInfo(soup)
    Database.Hochladen(data=meta_info, con=AldiSuedConnection, name='metainfo')
    
    angebote_urls = Produkt_URLs(urls = meta_info)
    
    
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
    ##### GANZ SPÄTER WIEDER EINKOMMENTIEREN UND SOUP IN DIE FOR SCHLEIFE ZIEHEN #####
    # for key, url in urls.items():
    #     if not url.startswith('https://'):
    #         continue
        
    # test url
    url = 'https://www.aldi-sued.de//de/angebote/d.06-10-2023.html'
    soup = Utils.lade_seite(url, include=['soup'])[0]
    
    
    # suche Kategorien
    labels = soup.find_all('span', class_='custom-control-description at-all-label-in-facetby-theme')
    kategorien = [label['data-description'] for label in labels]
    
    # kategorische urls, um Produkt-URLs nach Kategorien abzuifragen
    updated_urls = [url + '?sort=theme&theme=' + kat.replace(' ', '+') for kat in kategorien]
    
    
    # jetzt alle URLs ziehen, die je Kategorie auf der Seite liegen
    angebote_je_kategorie_urls = {}
    for kat_id, kat_url in enumerate(updated_urls):
        kat = kategorien[kat_id]
        soup = Utils.lade_seite(kat_url, include=['soup'])[0]
        angebote_je_kategorie_urls[kat] = get_categorical_urls(soup)
        
        
    Crawler(angebote_je_kategorie_urls)
    
    

def Crawler(angebote_je_kategorie_urls: dict):
    
    angebote_dict = defaultdict(list)

    # for kat, angebots_urls in angebote_je_kategorie_urls.items():
    #   for url in angebots_urls:
    test_url = 'https://www.aldi-sued.de/de/p.teekanne-wintertee--g.490300000000051634.html'
    CrawlURL(url = test_url, angebote_dict = angebote_dict)
    
    
def CrawlURL(url: str, angebote_dict: dict):
    angebot_soup = Utils.lade_seite(url, include=['soup'])[0]
    
    # jetzt beginnt das Inhalte Scraping
    name = find_element(angebot_soup, 'h1', 'at-productname_lbl target_product_name')
    preis = find_element(angebot_soup, 'span', 'pdp_price__now at-productprice_lbl')
    preis_hinweis = find_elements(angebot_soup, 'span', 'additional-notes-price') 
    # ...
    
    

def find_elements(soup, tag, class_name):
    elements = soup.find_all(tag, class_name)
    if elements:
        elements_strings = [e.text.strip() for e in elements]
        element = ', '.join(elements_strings)
        return element
    return ''
    
    
def find_element(soup, tag, class_name):
    element = soup.find(tag, class_name)
    if element:
        return element.text.strip()
    return ''



def get_categorical_urls(soup):
    url_prefix = 'https://www.aldi-sued.de'
    produkt_urls = []
    alle_artikel = soup.find_all('article', class_='wrapper')
    for artikel in alle_artikel:
        try:
            url_suffix = artikel.find('a').get('href')
            url = url_prefix + url_suffix
            produkt_urls.append(url)
        except:
            print(f'für Artikel {artikel} wurde keine url gefunden')
            continue
    return produkt_urls
        
    
    
    
    
        
