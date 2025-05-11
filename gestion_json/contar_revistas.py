import json

with open('datos/json/revistas.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
print("Total de revistas:", len(data))