'''
Scrapper para obtener informacion de resurchify
'''

import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

def construir_url_resurchify(nombre_revista):
    return f'https://www.resurchify.com/impact/details.php?q={quote(nombre_revista)}'

def get_span_after_strong(soup, texto_busqueda):
    for strong in soup.find_all('strong'):
        if texto_busqueda.lower() in strong.text.lower():
            span = strong.find_next('span')
            if span:
                return span.text.strip()
    return None

def extraer_historial(soup):
    tabla = soup.find('table', class_='borderTable')
    historial = []
    if tabla:
        headers = [th.text.strip().lower() for th in tabla.find_all('th')]
        for fila in tabla.find_all('tr')[1:]:  
            celdas = [td.text.strip() for td in fila.find_all('td')]
            if len(celdas) == len(headers):
                historial.append(dict(zip(headers, celdas)))
    return historial if historial else None

def extraer_info_resurchify(nombre_revista):
    url = construir_url_resurchify(nombre_revista)
    try:
        res = requests.get(url, headers=HEADERS, timeout=15)
        res.raise_for_status()
    except Exception as e:
        print(f"Error al acceder a Resurchify para '{nombre_revista}': {e}")
        return {}

    soup = BeautifulSoup(res.text, 'html.parser')

    info = {}

    # Impact Factor
    impact_tag = soup.find('div', class_='impact-factor')
    if impact_tag:
        info['impact_factor'] = impact_tag.text.strip()

    # Journal Impact Score 
    info['journal_impact_score'] = get_span_after_strong(soup, 'Journal Impact Score')

    # Historial detallado
    historial = extraer_historial(soup)
    if historial:
        info['detailed_history'] = historial

    return info
