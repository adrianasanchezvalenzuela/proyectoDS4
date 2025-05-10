import os
import json

base_path = "datos"
areas_folder = os.path.join(base_path, "csv", "areas")
catalogos_folder = os.path.join(base_path, "csv", "catalogos")
output_folder = os.path.join(base_path, "json")
output_file = os.path.join(output_folder, "revistas.json")

revistas = {}

def agregar_valor(diccionario, titulo, tipo, valor):
    if titulo not in diccionario:
        diccionario[titulo] = {"areas": [], "catalogos": []}
    if valor not in diccionario[titulo][tipo]:
        diccionario[titulo][tipo].append(valor)

for archivo in os.listdir(areas_folder):
    if archivo.endswith(".csv"):
        area = os.path.splitext(archivo)[0].upper().replace(" RADGRIDEXPORT", "")
        with open(os.path.join(areas_folder, archivo), "r", encoding="latin-1") as f:
            next(f) 
            for linea in f:
                titulo = linea.strip().lower()
                if titulo:
                    agregar_valor(revistas, titulo, "areas", area)


for archivo in os.listdir(catalogos_folder):
    if archivo.endswith(".csv"):
        catalogo = os.path.splitext(archivo)[0].upper().replace("_RADGRIDEXPORT", "")
        with open(os.path.join(catalogos_folder, archivo), "r", encoding="latin-1") as f:
            next(f)
            for linea in f:
                titulo = linea.strip().lower()
                if titulo:
                    agregar_valor(revistas, titulo, "catalogos", catalogo)


with open(output_file, "w", encoding="utf-8") as f:
    json.dump(revistas, f, indent=4, ensure_ascii=False)


with open(output_file, "r", encoding="utf-8") as f:
    data = json.load(f)
    print("JSON cargado exitosamente.")
    