'''
Programa principal para extraer información de revistas desde SCImago, por rangos
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

def main():
    parser = argparse.ArgumentParser(description="Scraper de SCImago por rangos")
    parser.add_argument('-a', '--archivo', required=True, help='Archivo JSON de entrada')
    parser.add_argument('-p', '--inicio', type=int, required=True, help='Índice inicial')
    parser.add_argument('-u', '--fin', type=int, required=True, help='Índice final (no incluido)')
    parser.add_argument('-o', '--salida', required=True, help='Archivo JSON de salida')
    args = parser.parse_args()

    revistas = cargar_revistas(args.archivo)
    nombres = list(revistas.keys())
    seleccionadas = nombres[args.inicio:args.fin]

    resultados = {}

    for nombre in seleccionadas:
        nombre_formateado = unidecode(nombre).title()
        print(f"Buscando: {nombre_formateado}")

        try:
            url_revista = obtener_url_revista(nombre_formateado)
            if not url_revista:
                print(f"No se encontró URL para: '{nombre_formateado}' (original: '{nombre}')")
                continue

            info = extraer_info_revista(url_revista)
            if info:
                resultados[nombre] = info

            time.sleep(2)

        except Exception as e:
            print(f"Error en '{nombre}': {e}")

    guardar_resultados(resultados, args.salida)
    print(f"Datos guardados en {args.salida}")

if __name__ == '__main__':
    main()
