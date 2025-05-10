'''
Scrapper para scimago
'''

import os
import json
import time
import requests
from bs4 import BeautifulSoup
from unidecode import unidecode
from urllib.parse import quote

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

def construir_url(nombre_revista):
    return f'https://www.scimagojr.com/journalsearch.php?q={quote(nombre_revista)}'

def cargar_revistas(archivo):
    with open(archivo, 'r', encoding='utf-8') as f:
        return json.load(f)

def cargar_datos_existentes(archivo):
    if os.path.exists(archivo):
        with open(archivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def guardar_resultados(datos, archivo_salida):
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)


def get_texto(soup, selector):
    el = soup.select_one(selector)
    return el.text.strip() if el else None

def obtener_sitio_web(soup):
    heading = soup.find('h2', string='Information')
    if heading:
        for a in heading.find_all_next('a', id='question_journal'):
            if 'Homepage' in a.text:
                return a['href'].strip()
    return None

def get_texto_por_h2(soup, titulo):
    h2 = soup.find('h2', string=titulo)
    if h2:
        p = h2.find_next('p')
        if p:
            return p.text.strip()
    return None

def obtener_imagen(soup):
    try:
        img = soup.find('img', class_='imgwidget')
        if img and 'src' in img.attrs:
            return 'https://www.scimagojr.com/' + img['src']
    except Exception as e:
        print(f"Error al extraer widget: {e}")
    return None

def obtener_url_revista(nombre_revista):
    url = construir_url(nombre_revista)
    res = requests.get(url, headers=HEADERS, timeout=15)
    soup = BeautifulSoup(res.text, 'html.parser')

    enlaces = soup.select(".search_results a[href*='journalsearch.php?q=']")
    for a in enlaces:
        href = a.get("href", "")
        if "tip=sid" in href:
            return 'https://www.scimagojr.com/' + href

    return None

def extraer_info_revista(url):
    res = requests.get(url, headers=HEADERS, timeout=15)
    soup = BeautifulSoup(res.text, 'html.parser')

    info = {
        'sitio_web': obtener_sitio_web(soup),
        'h_index': get_texto_por_h2(soup, "H-Index"),
        'subject_area': get_texto_por_h2(soup, 'Subject Area and Category'),
        'publisher': get_texto_por_h2(soup, 'Publisher'),
        'issn': get_texto_por_h2(soup, 'ISSN'),
        'widget': obtener_imagen(soup),
        'tipo_publicacion': get_texto_por_h2(soup, 'Publication type'),
        'ultima_visita': time.strftime("%Y-%m-%d")
    }

    return info

'''
# Prueba
def prueba_individual(nombre_original):
    
    nombre_limpio = unidecode(nombre_original)  # elimina tildes, diéresis, etc.
    nombre_formateado = ' '.join([palabra.capitalize() for palabra in nombre_limpio.split()])
    print(f"\nBuscando: {nombre_formateado}")

    url = obtener_url_revista(nombre_formateado)
    if not url:
        print(f"No se encontró URL para: {nombre_formateado}")
        return

    print(f"URL encontrada: {url}")
    info = extraer_info_revista(url)
    print(f"Información extraída para '{nombre_original}':\n")
    for k, v in info.items():
        print(f"  {k}: {v}") 

    '''
