import hashlib
from dataclasses import dataclass

@dataclass
class Usuario:
    username: str
    password: str  # Almacenará el hash
    nombre_completo: str
    favoritos: set = None

    def __post_init__(self):
        if self.favoritos is None:
            self.favoritos = set()

    def hash_string(self, s):
        """Genera hash SHA-256 de una cadena"""
        return hashlib.sha256(s.encode()).hexdigest()

    def verificar_password(self, password):
        """Verifica si el password coincide con el hash almacenado"""
        return self.hash_string(password) == self.password

class SistemaRevistas:
    def __init__(self):
        self.usuarios = {
            "admin": Usuario(
                username="admin",
                password=self.hash_string("admin123"),
                nombre_completo="Administrador del Sistema"
            ),
            "investigador": Usuario(
                username="investigador",
                password=self.hash_string("inv12345"),
                nombre_completo="Investigador UNISON"
            )
        }
        self.usuario_actual = None
        self.revistas = self._cargar_revistas_ejemplo()

    @staticmethod
    def hash_string(s):
        """Genera hash SHA-256 de una cadena"""
        return hashlib.sha256(s.encode()).hexdigest()

    def _cargar_revistas_ejemplo(self):
        """Carga datos de ejemplo de revistas"""
        return [
            {
                "id": 1,
                "titulo": "Journal of Materials Science",
                "areas": ["Ciencias Exactas", "Ingenierías"],
                "catalogos": ["Q1", "SCIE"],
                "h_index": 45,
                "descripcion": "Revista líder en ciencia de materiales..."
            },
            # ... más revistas
        ]

    def login(self, username, password):
        """Inicia sesión en el sistema"""
        if username in self.usuarios:
            user = self.usuarios[username]
            if user.verificar_password(password):
                self.usuario_actual = user
                return True
        return False

    def logout(self):
        """Cierra la sesión actual"""
        self.usuario_actual = None

    def agregar_favorito(self, revista_id):
        """Agrega una revista a favoritos del usuario actual"""
        if self.usuario_actual:
            self.usuario_actual.favoritos.add(revista_id)
            return True
        return False

    def eliminar_favorito(self, revista_id):
        """Elimina una revista de favoritos"""
        if self.usuario_actual and revista_id in self.usuario_actual.favoritos:
            self.usuario_actual.favoritos.remove(revista_id)
            return True
        return False

    def obtener_favoritos(self):
        """Devuelve las revistas favoritas del usuario actual"""
        if not self.usuario_actual:
            return []
        
        return [r for r in self.revistas if r["id"] in self.usuario_actual.favoritos]

    def buscar_revistas(self, query):
        """Busca revistas por título"""
        return [r for r in self.revistas if query.lower() in r["titulo"].lower()]