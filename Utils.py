import undetected_chromedriver as uc
import requests
from bs4 import BeautifulSoup

def lade_seite(url: str, include: list=['driver', 'soup']) -> list:
    '''TODO driver laden klappt aktuell nicht ...
    '''
    url = url + '.html'
    return_elements = []
    
    if 'driver' in include:
        driver = uc.Chrome()
        driver.get(url)
        return_elements.append(driver)
    
    if 'soup' in include:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            return_elements.append(soup)
        
    assert (len(return_elements) != 0), 'Es gab einen Fehler beim Laden der Seite.'
    return return_elements