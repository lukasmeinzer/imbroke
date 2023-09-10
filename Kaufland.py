import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import requests
from bs4 import BeautifulSoup


def lade_seite(url):
    url = url + '.html'
    driver = uc.Chrome()
    driver.get(url)
    
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
    else:
        soup = None
        
    return soup, driver


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
        kategorien_urls.append(kategorie_url)
    
    return kategorien_urls


def Angebote(kategorien_urls: list):
    for url in kategorien_urls:
        response = requests.get(url)
        
        assert response.status_code == 200, 'Fehler beim Verbinden mit einer Kategorien-URL'
        
        kat_soup = BeautifulSoup(response.text, 'html.parser')
        
        
        