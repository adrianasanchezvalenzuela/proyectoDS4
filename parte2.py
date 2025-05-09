'''
Scrapper 
'''

import os
import json
import time
import requests
from bs4 import BeautifulSoup

def cargar_json_entrada(ruta):
    with open(ruta, 'r', encoding='utf-8') as f:
        return json.load(f)

def guardar_json_salida(datos, ruta):
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

def obtener_info_revista(nombre_revista):
    url = f"https://www.scimagojr.com/journalsearch.php?q={nombre_revista.replace(' ', '+')}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    resp = requests.get(url, headers=headers, timeout=10)

    if resp.status_code != 200:
        print(f"Error al acceder a {url}")
        return None

    soup = BeautifulSoup(resp.content, 'html.parser')
    enlace_revista = soup.select_one("a[href^='journalrank.php?']")

    if not enlace_revista:
        print(f"No se encontró la revista: {nombre_revista}")
        return None

    url_revista = f"https://www.scimagojr.com/{enlace_revista['href']}"
    resp = requests.get(url_revista, headers=headers, timeout=10)

    if resp.status_code != 200:
        print(f"Error al acceder a {url_revista}")
        return None

    soup = BeautifulSoup(resp.content, 'html.parser')

    datos = {
        "website": None,
        "h_index": None,
        "subject_area": None,
        "publisher": None,
        "issn": None,
        "widget": None,
        "publication_type": None
    }

    try:
        # Sitio web
        link = soup.find("a", string="Homepage")
        if link:
            datos["website"] = link.get("href")

        # H-index
        h_index = soup.find(text="H index")
        if h_index:
            datos["h_index"] = h_index.find_next("span").text.strip()

        # Subject Area and Category
        sa = soup.find("div", class_="journaldescription").find("h2")
        if sa:
            datos["subject_area"] = sa.text.strip()

        # Publisher
        datos["publisher"] = soup.find(text="Publisher").find_next("span").text.strip()

        # ISSN
        datos["issn"] = soup.find(text="ISSN").find_next("span").text.strip()

        # Widget
        widget = soup.find("textarea", {"id": "scimagowidget"})
        if widget:
            datos["widget"] = widget.text.strip()

        # Publication Type
        datos["publication_type"] = soup.find(text="Type").find_next("span").text.strip()

    except Exception as e:
        print(f"Error extrayendo datos de {nombre_revista}: {e}")
        return None

    return datos

def scrapear_revistas(json_entrada, json_salida):
    revistas = cargar_json_entrada(json_entrada)
    resultados = {}

    if os.path.exists(json_salida):
        with open(json_salida, 'r', encoding='utf-8') as f:
            resultados = json.load(f)

    for nombre, datos in revistas.items():
        if nombre in resultados:
            print(f"{nombre} ya scrapeado, se omite.")
            continue

        print(f"Scrapeando {nombre}...")
        info = obtener_info_revista(nombre)
        if info:
            resultados[nombre] = {**datos, **info}
            guardar_json_salida(resultados, json_salida)
            time.sleep(2)  # Para no saturar el servidor
        else:
            print(f"No se pudo obtener info para {nombre}")

    print("Scrapeo finalizado.")

if __name__ == '__main__':
    path_entrada = 'data/json/revistas.json'        # Ruta al JSON con nombres de revistas (parte 1)
    path_salida = 'data/json/detalles_revistas.json'  # Ruta donde se guardará la info scrapeada

    scrapear_revistas(path_entrada, path_salida)
