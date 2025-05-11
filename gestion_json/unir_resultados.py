import json

archivos = ['datos/json/salida_A.json', 'datos/json/salida_A2.json', 'datos/json/revistas_info_parte_1.json', 'datos/json/salida_E.json']
resultado = {}

for archivo in archivos:
    with open(archivo, 'r', encoding='utf-8') as f:
        datos = json.load(f)
        resultado.update(datos)

with open('datos/json/revistas_info_scimago.json', 'w', encoding='utf-8') as f:
    json.dump(resultado, f, indent=2, ensure_ascii=False)

print("Resultados guardados correctamente :)")