import json
import csv
import hashlib
import re
from dataclasses import dataclass, field
from typing import Set, Dict, List


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
    def __init__(self, id_revista, titulo, issn, editor, h_index, descripcion, url, tipo_publicacion, areas=None):
        self.id_revista = id_revista
        self.titulo = titulo
        self.issn = issn
        self.editor = editor
        self.h_index = h_index
        self.descripcion = descripcion
        self.url = url
        self.tipo_publicacion = tipo_publicacion
        self.areas = areas or []

    def __str__(self):
        return (
            f"ID: {self.id_revista}\n"
            f"Título: {self.titulo}\n"
            f"ISSN: {self.issn}\n"
            f"Editor: {self.editor}\n"
            f"Tipo_publicación: {self.tipo_publicacion}\n"
            f"Áreas: {', '.join(self.areas)}\n"
            f"H-index: {self.h_index}\n"
            f"Descripción: {self.descripcion}\n"
            f"URL: {self.url}"
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
                        areas=areas
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
    def imprimir_revistas_por_area(revistas: List["Revista"], titulos_por_area: Dict[str, Set[str]]):
        """Imprime las revistas clasificadas por área"""
        print("\n=== REVISTAS AGRUPADAS POR ÁREA ===\n")

        for area, titulos_area in titulos_por_area.items():
            print(f"\nÁrea: {area.upper()}")
            print("-" * 60)
            encontradas = 0

            for revista in revistas:
                if revista.titulo.strip().lower() in titulos_area:
                    print(revista)
                    print("-" * 60)
                    encontradas += 1

            if encontradas == 0:
                print("No se encontraron revistas para esta área.")




class SistemaRevistas:
    def __init__(self):
        self.revistas = []
        self.titulos_por_area = {}
        self.usuarios: List[Usuario] = []  # Solo si los usas
        self.usuario_actual: Usuario | None = None  # Opcional

    def cargar_datos(self, json_path: str, carpeta_csv: str):
        self.revistas = Revista.cargar_revistas_desde_json(json_path)
        self.titulos_por_area = Revista.cargar_titulos_por_area(carpeta_csv)

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


def main():
    json_path = "datos/json/revistas_info_parte_1.json"
    carpeta_csv = "datos/csv/areas"

    # Cargar las revistas desde JSON
    revistas = Revista.cargar_revistas_desde_json(json_path)

    if revistas:
        print(f"\nTotal de revistas cargadas: {len(revistas)}\n")
        for revista in revistas[:2]:
            print(revista)
            print("\n" + "-" * 50 + "\n")
    else:
        print("No se cargaron revistas.")

    # Cargar títulos por área desde CSV
    titulos_por_area = Revista.cargar_titulos_por_area(carpeta_csv)

    for area, titulos in titulos_por_area.items():
        print(f"{area}: {len(titulos)} títulos")
        for titulo in list(titulos)[:5]:  # Puedes ajustar este número
            print(f"  - {titulo}")
    print("-" * 50)
    Revista.imprimir_revistas_por_area(revistas, titulos_por_area)




if __name__ == "__main__":
    main()