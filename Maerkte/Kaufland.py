
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import pandas as pd
from tqdm import tqdm
import Database
import Utils


def AllKaufland(url: str):
    KauflandConnection = Database.KauflandDB()

    soup = Utils.lade_seite(url, include=['soup'])[0]
    # keks_klicker(driver)

    meta_info = MetaInfo(soup)
    Database.Hochladen(data=meta_info, con=KauflandConnection, name='metainfo')

    kategorien = Kategorien(soup)
    kategorien_urls = Kategorien_URLs(kategorien, url)

    angebote_je_kategorie_urls = Produkt_URLs(kategorien_urls)
    angebote = Crawler(angebote_je_kategorie_urls)
    Database.Hochladen(data=angebote, con=KauflandConnection, name='angebote')




def keks_klicker(driver):
    cookie = driver.find_element(By.ID,value='onetrust-reject-all-handler')
    actions = ActionChains(driver)
    actions.click(on_element=cookie)
    actions.perform()


def MetaInfo(soup):
    aktuelle_woche = soup.find('h1', class_='a-headline a-headline--level-1-responsive', attrs={'data-t-name': 'Headline'})
    if aktuelle_woche:
        aktuelle_woche = aktuelle_woche.text.strip()
    
    meta_info = soup.find(class_='t-typography__title-sub-3')
    if meta_info:
        meta_info = meta_info.text.strip()
    
    meta_info_zusammenfassend = {
        'Woche': [aktuelle_woche],
        'Info': [meta_info]
    }
    return meta_info_zusammenfassend
    
    
    
def Kategorien(soup):
    kategorien = soup.find_all('h2', class_='o-richtext--level-2')
    if kategorien:  
        kategorien = [(i, kat.text.strip()) for i, kat in enumerate(kategorien)]
        return kategorien
    return []
        
        
def Kategorien_URLs(kategorien: list, url: str, exclude=['Drogerie, Tiernahrung', 'Elektro, Büro, Medien', 'Heim, Haus', 'Bekleidung, Auto, Freizeit, Spiel']) -> list:
    fisch = False
    kategorien_urls = []
    for kat_nummer, kategorie in kategorien:
        if kategorie in exclude:
            continue
        if not fisch:
            kat_nummer += 1
        if kategorie == 'Fisch':
            fisch = True
            kat_nummer = '01a'
            kategorie = 'Frischer_Fisch'
        kategorie_url = url + '/uebersicht.category=' + str(kat_nummer).zfill(2) + '_' + kategorie.replace(', ', '__') + '.html'
        kategorien_urls.append((kategorie, kategorie_url))
    
    return kategorien_urls


def Produkt_URLs(kategorien_urls: list):
    
    angebote_je_kategorie = {}
    
    for kat, kat_url in kategorien_urls:
        
        produkt_urls = []
        
        response = requests.get(kat_url)
        
        assert response.status_code == 200, 'Fehler beim Verbinden mit einer Kategorien-URL'
        
        kat_soup = BeautifulSoup(response.text, 'html.parser')
        alle_angebote = kat_soup.find_all('a', 'm-offer-tile__link u-button--hover-children')
        for angebot in alle_angebote:
            produkt_urls.append(angebot.get('href'))
        
        angebote_je_kategorie[kat] = produkt_urls
        
    return angebote_je_kategorie


def Crawler(angebote_je_kategorie_urls: dict):
    url_prefix = 'https://filiale.kaufland.de'
    
    angebote_dict = defaultdict(list)
    
    for kat, angebot_urls in angebote_je_kategorie_urls.items():
        for url in tqdm(angebot_urls):
            url = url_prefix + url
            angebote_dict['Kategorie'].append(kat)
            CrawlURL(url, angebote_dict)
    try:
        angebote_df = pd.DataFrame(angebote_dict)
    except Exception:
        print('Fehler beim Crawling Inhalt...')
    
    return angebote_df
        
        
def CrawlURL(url: str, angebote_dict: defaultdict):
    response = requests.get(url)
    assert response.status_code == 200, 'Fehler beim Verbinden mit einer Angebots-URL'
    
    angebot_soup = BeautifulSoup(response.text, 'html.parser')
    
    #TODO: Wenn Angebot nicht mehr verfügbar
    # Beispiel: '/angebote/aktuelle-woche/uebersicht/detail.so_id=00014234.html'
    
    image_source = find_element(angebot_soup, 'img', 'a-image-responsive a-image-responsive--preview-knockout')
    if image_source != '':
        image_source = image_source.get('src')
    gueltigkeit = find_element(angebot_soup, 'span', 'a-eye-catcher__text')
    hersteller = find_element(angebot_soup, 'h2', 't-offer-detail__subtitle')
    name = find_element(angebot_soup, 'h1', 't-offer-detail__title')
    beschreibung = find_element(angebot_soup, 'div', 't-offer-detail__description')
    mengen_einheit = find_element(angebot_soup, 'div', 't-offer-detail__quantity')
    angebots_detail = find_element(angebot_soup, 'div', 't-offer-detail__mpa')
    angebots_detail_basis_preis = find_element(angebot_soup, 'div', 't-offer-detail__basic-price')
    angebots_detail_minimum = find_element(angebot_soup, 'div', 't-offer-detail__minimum')
    preis_discount = find_element(angebot_soup, 'div', 'a-pricetag__discount')
    preis_alt = find_element(angebot_soup, 'span', 'a-pricetag__old-price a-pricetag__line-through')
    preis_waehrung = find_element(angebot_soup, 'span', 'a-pricetag__currency')
    preis_neu = find_element(angebot_soup, 'div', 'a-pricetag__price')
    angebots_hinweis = find_element(angebot_soup, 'div', 't-offer-detail__notification')
    
    
    angebote_dict['Image'].append(image_source)
    angebote_dict['Gültigkeit'].append(gueltigkeit)
    angebote_dict['Hersteller'].append(hersteller)
    angebote_dict['Produkt_Name'].append(name)
    angebote_dict['Beschreibung'].append(beschreibung)
    angebote_dict['ME'].append(mengen_einheit)
    angebote_dict['Detail'].append(angebots_detail)
    angebote_dict['Basis_Preis'].append(angebots_detail_basis_preis)
    angebote_dict['Minimum'].append(angebots_detail_minimum)
    angebote_dict['Discount'].append(preis_discount)
    angebote_dict['Preis_Alt'].append(preis_alt)
    angebote_dict['Preis_Neu'].append(preis_neu)
    angebote_dict['Währung'].append(preis_waehrung)
    angebote_dict['Hinweis'].append(angebots_hinweis)
    
    return angebote_dict
    
    
def find_element(soup, tag, class_name):
        element = soup.find(tag, class_name)
        if element:
            return element.text.strip()
        return ''