'''
Programa principal para extraer información de revistas desde scimago y resurchify
'''

import argparse
import time
from unidecode import unidecode
from scimago_scrapper import (
    cargar_revistas,
    guardar_resultados,
    extraer_info_revista,
    obtener_url_revista
)
from resurchify_scrapper import extraer_info_resurchify

def main():
    parser = argparse.ArgumentParser(description="Scraper combinado de scimago y resurchify por rangos")
    parser.add_argument('-a', '--archivo', required=True, help='Archivo JSON de entrada')
    parser.add_argument('-p', '--inicio', type=int, required=True, help='Indice inicial')
    parser.add_argument('-u', '--fin', type=int, required=True, help='Indice final (no incluido)')
    parser.add_argument('-o', '--salida', required=True, help='Archivo JSON de salida')
    args = parser.parse_args()

    revistas = cargar_revistas(args.archivo)
    nombres = list(revistas.keys())
    seleccionadas = nombres[args.inicio:args.fin]

    resultados = {}

    total = len(seleccionadas)

    for i, nombre in enumerate(seleccionadas, start=1):
        nombre_formateado = unidecode(nombre).title()
        print(f"[{i}/{total}] Buscando: {nombre_formateado}")

        try:
            # Info de scimago
            url_revista = obtener_url_revista(nombre_formateado)
            if not url_revista:
                print(f"No se encontró URL SCImago para: '{nombre_formateado}'")
                continue

            info_scimago = extraer_info_revista(url_revista)

            # Info de resurchify
            info_resurchify = extraer_info_resurchify(nombre_formateado)

            # Aqui se combina la información
            info_completa = {**info_scimago, **info_resurchify}
            resultados[nombre] = info_completa

            time.sleep(2)

        except Exception as e:
            print(f"Error en '{nombre}': {e}")

    guardar_resultados(resultados, args.salida)
    print(f"Datos guardados en {args.salida}")

if __name__ == '__main__':
    main()
