import json
import csv
import hashlib
import re
from dataclasses import dataclass, field
from typing import Set, Dict, List
from collections import defaultdict


# Constante global para las rutas CSV
AREAS_CSV = {
    'ciencias_bio': 'datos/csv/areas/CIENCIAS_BIO RadGridExport.csv',
    'ciencias_eco': 'datos/csv/areas/CIENCIAS_ECO RadGridExport.csv',
    'ciencias_exa': 'datos/csv/areas/CIENCIAS_EXA RadGridExport.csv',
    'ciencias_soc': 'datos/csv/areas/CIENCIAS_SOC RadGridExport.csv',
    'ed_inst': 'datos/csv/areas/ED_INST RadGridExport.csv',
    'ed_lib': 'datos/csv/areas/ED_LIB RadGridExport.csv',
    'human_y_art': 'datos/csv/areas/HUMAN_Y_ART RadGridExport.csv',
    'ing': 'datos/csv/areas/ING RadGridExport.csv',
    'multi': 'datos/csv/areas/MULTI RadGridExport.csv',
}

CATALOGOS_CSV = {
    'CONACYT': 'datos/csv/catalogos/CONACYT_RadGridExport.csv',
    'JCR': 'datos/csv/catalogos/JCR_RadGridExport.csv',
    'MLA': 'datos/csv/catalogos/MLA_RadGridExport.csv',
    'SCIELO': 'datos/csv/catalogos/SCIELO_RadGridExport.csv',
    'SCOPUS': 'datos/csv/catalogos/SCOPUS_RadGridExport.csv',
}



@dataclass
class Usuario:
    """Clase para manejar usuarios del sistema"""
    username: str
    password: str  # Almacena el hash
    nombre_completo: str
    email: str
    favoritos: Set[int] = field(default_factory=set)

    @staticmethod
    def hash_string(s: str) -> str:
        """Genera hash SHA-256 de una cadena"""
        return hashlib.sha256(s.encode()).hexdigest()

    def verificar_password(self, password: str) -> bool:
        """Verifica si el password coincide con el hash almacenado"""
        return self.hash_string(password) == self.password


class Revista:
    def __init__(self, id_revista, titulo, issn, editor, h_index, descripcion, url, tipo_publicacion, areas=None, catalogo=None, seccion=None):
        self.id_revista = id_revista
        self.titulo = titulo
        self.issn = issn
        self.editor = editor
        self.h_index = h_index
        self.descripcion = descripcion
        self.url = url
        self.tipo_publicacion = tipo_publicacion
        self.areas = areas if areas else []  # Lista de áreas
        self.catalogo = catalogo or "No disponible"
        self.seccion = seccion or "No disponible"  # Sección como una cadena de texto


    def __str__(self):
        return (
            f"ID: {self.id_revista}\n"
            f"Título: {self.titulo}\n"
            f"ISSN: {self.issn}\n"
            f"Editor: {self.editor}\n"
            f"Tipo_publicación: {self.tipo_publicacion}\n"
            f"Áreas: {self.areas}\n"
            f"H-index: {self.h_index}\n"
            f"Descripción: {self.descripcion}\n"
            f"URL: {self.url}"
            f"\nCatálogo: {self.catalogo}\n"
            f"Sección: {self.seccion}\n"
        )

    @staticmethod
    def cargar_revistas_desde_json(json_path: str) -> List['Revista']:
        """Carga revistas desde un archivo JSON"""
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
                        areas=areas,
                        catalogo=revista_data.get("catalogo", "No disponible"),
                        seccion=revista_data.get("seccion", "No disponible")
                    )

                    revistas.append(revista)
                    contador_id += 1

                return revistas

        except Exception as e:
            print(f"Error cargando el archivo JSON: {str(e)}")
            return []

    @staticmethod
    def cargar_titulos_por_area(carpeta_csv: str) -> Dict[str, Set[str]]:
        """Carga títulos de revistas por área desde archivos CSV"""
        titulos_por_area = {}

        for codigo, ruta_csv in AREAS_CSV.items():
            try:
                with open(ruta_csv, mode='r', encoding='latin1') as archivo:
                    lector = csv.DictReader(archivo)
                    titulos = set()
                    for fila in lector:
                        titulo = fila.get('TITULO:', '').strip().lower()
                        if titulo:
                            titulos.add(titulo)
                    titulos_por_area[codigo] = titulos
            except Exception as e:
                print(f"Error con {ruta_csv}: {e}")
                titulos_por_area[codigo] = set()

        return titulos_por_area

    
    @staticmethod
    def cargar_titulos_por_catalogo(carpeta_catalogos: str) -> Dict[str, Set[str]]:
        """Carga títulos de revistas por catálogo desde archivos CSV"""
        titulos_por_catalogo = {}

        for nombre, ruta_csv in CATALOGOS_CSV.items():
            try:
                with open(ruta_csv, mode='r', encoding='latin1') as archivo:
                    lector = csv.DictReader(archivo)
                    titulos = set()
                    for fila in lector:
                        titulo = fila.get('TITULO:', '').strip().lower()
                        if titulo:
                            titulos.add(titulo)
                    titulos_por_catalogo[nombre] = titulos
            except Exception as e:
                print(f"Error con {ruta_csv}: {e}")
                titulos_por_catalogo[nombre] = set()

        return titulos_por_catalogo
    
    @staticmethod
    def imprimir_revistas_por_catalogo(revistas: List["Revista"], titulos_por_catalogo: Dict[str, Set[str]]):
        """Imprime las revistas clasificadas por catálogo"""
        print("\n=== REVISTAS AGRUPADAS POR CATÁLOGO ===\n")

        for catalogo, titulos in titulos_por_catalogo.items():
            print(f"\nCatálogo: {catalogo.upper()}")
            print("-" * 60)
            encontradas = 0

            for revista in revistas:
                if revista.titulo.strip().lower() in titulos:
                    print(revista)
                    print("-" * 60)
                    encontradas += 1

            if encontradas == 0:
                print("No se encontraron revistas para este catálogo.")

        for revista in revistas:
            catalogo = revista.catalogo.strip().upper()
            titulos = titulos_por_catalogo.get(catalogo)
            if titulos is None:
                print(f"[!] Catálogo no encontrado: '{revista.catalogo}'")

    @staticmethod
    def clasificar_revistas_por_catalogo(revistas: List["Revista"], titulos_por_catalogo: Dict[str, Set[str]]):
        """Asigna el nombre del catálogo correcto a cada revista si se encuentra"""
        for revista in revistas:
            titulo_normalizado = revista.titulo.strip().lower()
            encontrado = False
            for catalogo, titulos in titulos_por_catalogo.items():
                if titulo_normalizado in titulos:
                    revista.catalogo = catalogo
                    encontrado = True
                    break
            if not encontrado:
                revista.catalogo = "No disponible"

    @staticmethod
    def clasificar_revistas_por_area(revistas: List["Revista"], titulos_por_area: Dict[str, Set[str]]):
        """Clasifica revistas por área y asigna el área principal correspondiente"""
        for revista in revistas:
            titulo_normalizado = revista.titulo.strip().lower()
            
            # Crear una lista temporal para las áreas encontradas
            areas_encontradas = []

            # Buscar en las áreas y agregar a la lista temporal
            for area, titulos in titulos_por_area.items():
                if titulo_normalizado in titulos:
                    areas_encontradas.append(area)

            # Si no se encontraron áreas, asignar "No disponible"
            if not areas_encontradas:
                areas_encontradas.append("No disponible")

            # Asignar las áreas encontradas a 'area' como una cadena separada por comas
            revista.area = ", ".join(areas_encontradas)
            
            # No se modifica la lista 'areas', esta sigue siendo una lista separada



    @staticmethod
    def clasificar_revistas_por_area(revistas: List["Revista"], titulos_por_area: Dict[str, Set[str]]):
        """Clasifica revistas por área y asigna la sección correspondiente"""
        for revista in revistas:
            titulo_normalizado = revista.titulo.strip().lower()
            
            # Crear una lista temporal para las áreas encontradas
            areas_encontradas = []

            # Buscar en las áreas y agregar a la lista temporal
            for area, titulos in titulos_por_area.items():
                if titulo_normalizado in titulos:
                    areas_encontradas.append(area)

            # Si no se encontraron áreas, asignar "No disponible"
            if not areas_encontradas:
                areas_encontradas.append("No disponible")

            # Asignar las áreas encontradas a 'seccion' como una cadena separada por comas
            revista.seccion = ", ".join(areas_encontradas)
            

    def clasificar_revistas_por_letra(revistas: List["Revista"]) -> Dict[str, List["Revista"]]:
        """Clasifica las revistas por la primera letra de su título."""
        revistas_por_letra = defaultdict(list)

        for revista in revistas:
            # Obtenemos la primera letra del título de la revista (en minúsculas)
            letra_inicial = revista.titulo.strip()[0].upper()

            # Verificamos que la letra sea una letra válida (A-Z)
            if letra_inicial.isalpha():
                revistas_por_letra[letra_inicial].append(revista)

        return dict(revistas_por_letra)

class SistemaRevistas:
    def __init__(self):
        self.revistas = []
        self.titulos_por_area = {}
        self.usuarios: List[Usuario] = []  # Solo si los usas
        self.usuario_actual: Usuario | None = None  # Opcional

    def cargar_datos(self, json_path: str, carpeta_csv: str, carpeta_catalogos: str):
        self.revistas = Revista.cargar_revistas_desde_json(json_path)
        self.titulos_por_area = Revista.cargar_titulos_por_area(carpeta_csv)
        self.titulos_por_catalogo = Revista.cargar_titulos_por_catalogo(carpeta_catalogos)
        
        # Clasifica revistas por catálogo justo después de cargarlas
        Revista.clasificar_revistas_por_catalogo(self.revistas, self.titulos_por_catalogo)
        # Clasifica revistas por área justo después de cargarlas
        Revista.clasificar_revistas_por_area(self.revistas, self.titulos_por_area)
        # Clasifica revistas por letra
        Revista.clasificar_revistas_por_letra(self.revistas)


    def obtener_revistas_por_area(self, area: str) -> List[Revista]:
        titulos = self.titulos_por_area.get(area, set())
        return [r for r in self.revistas if r.titulo.strip().lower() in titulos]

    def buscar_revistas(self, query: str) -> List[Revista]:
        query = query.lower()
        return [r for r in self.revistas if query in r.titulo.lower()]
    
    def obtener_revista_por_id(self, id_revista: int) -> Revista | None:
        for revista in self.revistas:
            if revista.id_revista == id_revista:
                return revista
        return None
    
    def obtener_revista_por_catalogo(self, catalogo: str) -> List[Revista]:
        return [revista for revista in self.revistas if revista.catalogo.strip().lower() == catalogo.lower()]
    
    def clasificar_revistas_por_letra(self, revistas):
        """Clasifica las revistas por la primera letra de su título."""
        revistas_por_letra = defaultdict(list)
        for revista in revistas:
            letra_inicial = revista.titulo.strip()[0].upper()
            if letra_inicial.isalpha():
                revistas_por_letra[letra_inicial].append(revista)
        return dict(revistas_por_letra)




def main():
    json_path = "datos/json/revistas_info_parte_1.json"
    carpeta_csv_areas = "datos/csv/areas"
    carpeta_csv_catalogos = "datos/csv/catalogos"

    # Paso 1: Cargar las revistas desde JSON
    revistas = Revista.cargar_revistas_desde_json(json_path)
    if not revistas:
        print("No se cargaron revistas.")
        return

    print(f"\nTotal de revistas cargadas: {len(revistas)}\n")
    for revista in revistas[:2]:  # Muestra un par como ejemplo
        print(revista)
        print("\n" + "-" * 50 + "\n")

    # Paso 2: Cargar títulos por área y por catálogo desde CSV
    titulos_por_area = Revista.cargar_titulos_por_area(carpeta_csv_areas)
    catalogos = Revista.cargar_titulos_por_catalogo(carpeta_csv_catalogos)

    # Paso 3: Asignar catálogos y áreas a las revistas
    Revista.clasificar_revistas_por_catalogo(revistas, catalogos)
    Revista.clasificar_revistas_por_area(revistas, titulos_por_area)

    # Paso 4: Imprimir resultados organizados
    print("\n" + "=" * 50)
    print("REVISTAS CON CATÁLOGO Y ÁREA ASIGNADOS")
    print("=" * 50 + "\n")

    for revista in revistas[:10]:  # Cambia el rango si quieres ver más
        print(revista)
        print("-" * 50)

    # Paso 5 (opcional): Mostrar resumen de áreas y catálogos
    print("\nResumen de áreas:")
    for area, titulos in titulos_por_area.items():
        print(f"{area}: {len(titulos)} títulos")
        for titulo in list(titulos)[:3]:
            print(f"  - {titulo}")

    print("\nResumen de catálogos:")
    for catalogo, titulos in catalogos.items():
        print(f"{catalogo}: {len(titulos)} títulos")
        for titulo in list(titulos)[:3]:
            print(f"  - {titulo}")



if __name__ == "__main__":
    main()