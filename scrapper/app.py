'''
Programa principal para extarer informacion de revistas desde scimago
'''

import time
from unidecode import unidecode
from scimago_scrapper import (
    cargar_revistas,
    cargar_datos_existentes,
    guardar_resultados,
    obtener_url_revista,
    extraer_info_revista
)

ENTRADA_JSON = 'datos/json/prueba.json'
SALIDA_JSON = 'datos/json/prueba_info.json'

def main():
    revistas = cargar_revistas(ENTRADA_JSON)
    resultados = cargar_datos_existentes(SALIDA_JSON)

    for nombre in revistas:
        if nombre in resultados:
            continue

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

    guardar_resultados(resultados, SALIDA_JSON)
    print(f"Datos guardados en {SALIDA_JSON}")

if __name__ == '__main__':
    main()
