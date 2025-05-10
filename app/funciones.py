# funciones.py
"""Clases para manejar la base de datos de revistas académicas"""
import json
import csv
import os
import hashlib
from dataclasses import dataclass, field
from typing import List, Dict, Set, Optional

@dataclass
class Usuario:
    """Clase para manejar usuarios del sistema"""
    username: str
    password: str  # Almacena el hash
    nombre_completo: str
    email: str
    favoritos: Set[int] = field(default_factory=set)  # IDs de revistas favoritas
    
    @staticmethod
    def hash_string(s: str) -> str:
        """Genera hash SHA-256 de una cadena"""
        return hashlib.sha256(s.encode()).hexdigest()

    def verificar_password(self, password: str) -> bool:
        """Verifica si el password coincide con el hash almacenado"""
        return self.hash_string(password) == self.password
    
    def verificar_password(self, password: str) -> bool:
        """Verifica si el password coincide con el hash almacenado"""
        return self.hash_string(password) == self.password
    


class Revista:
    def __init__(self, id_revista, titulo, issn, editor, h_index, descripcion, url, tipo_publicacion, areas=None):
        self.id_revista = id_revista
        self.titulo = titulo
        self.issn = issn
        self.editor = editor
        self.h_index = h_index
        self.descripcion = descripcion
        self.url = url
        self.tipo_publicacion = tipo_publicacion
        self.areas = areas

    def __str__(self):
        return f"ID: {self.id_revista}\nTítulo: {self.titulo}\nISSN: {self.issn}\nEditor: {self.editor}\nTipo_publicación: {self.tipo_publicacion}\nÁreas: {', '.join(self.areas)}\nH-index: {self.h_index}\nDescripción: {self.descripcion}\nURL: {self.url}"

def cargar_revistas_desde_json(json_path):
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            datos = json.load(f)
            revistas = []
            contador_id = 1

            for titulo, revista_data in datos.items():
                issn = revista_data.get("issn", "No disponible")
                editor = revista_data.get("publisher", "No disponible")
                tipo = revista_data.get("tipo_publicacion", "No disponible")

                raw_h_index = revista_data.get("h_index", 0)
                try:
                    h_index = int(raw_h_index) if raw_h_index is not None else 0
                except ValueError:
                    h_index = 0

                descripcion = revista_data.get("widget", "No disponible")
                url = revista_data.get("sitio_web", "No disponible")

                # Separar áreas por mayúsculas internas o comas
                import re
                subject_area_raw = revista_data.get("subject_area", "")
                if isinstance(subject_area_raw, str):
                    areas = re.split(r'(?<=[a-z])(?=[A-Z])|,', subject_area_raw)
                    areas = [a.strip() for a in areas if a.strip()]
                else:
                    areas = []

                revista = Revista(
                    id_revista=contador_id,
                    titulo=titulo,
                    issn=issn,
                    editor=editor,
                    h_index=h_index,
                    descripcion=descripcion,
                    url=url,
                    tipo_publicacion=tipo,
                    areas=areas
                )
                revistas.append(revista)
                contador_id += 1

            return revistas

    except Exception as e:
        print(f"Error cargando el archivo JSON: {str(e)}")
        return []




def main():
    # Ruta al archivo JSON
    json_path = "datos/json/salida_B.json"  # Cambia esto por el path real de tu archivo JSON
    
    # Cargar las revistas desde el archivo JSON
    revistas = cargar_revistas_desde_json(json_path)
    
    # Verificar si se cargaron revistas
    if revistas:
        print(f"\nTotal de revistas cargadas: {len(revistas)}\n")
        
        # Imprimir las primeras 2 revistas
        for revista in revistas[:2]:  # Solo mostrar las primeras 2 revistas
            print(revista)
            print("\n" + "-"*50 + "\n")
    else:
        print("No se cargaron revistas.")

# Ejecutar el programa
if __name__ == "__main__":
    main()