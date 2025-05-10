import json

archivos = ['datos/json/salida_B.json', 'datos/json/salida_C.json', 'datos/json/salida_D.json']
resultado = {}

for archivo in archivos:
    with open(archivo, 'r', encoding='utf-8') as f:
        datos = json.load(f)
        resultado.update(datos)

with open('datos/json/revistas_info_parte_1.json', 'w', encoding='utf-8') as f:
    json.dump(resultado, f, indent=2, ensure_ascii=False)

print("✅ Todos los resultados se han unido correctamente en 'revistas_info_completo.json'")