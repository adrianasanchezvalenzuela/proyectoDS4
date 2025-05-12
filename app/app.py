from flask import Flask, render_template, request, redirect, url_for, session, flash
from funciones import SistemaRevistas
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY') or 'clave-secreta'

# Inicializa el sistema
sistema = SistemaRevistas()
sistema.cargar_datos("datos/json/revistas_info_scimago.json", "datos/csv/areas", "datos/csv/catalogos")
sistema.cargar_usuarios_desde_csv("datos/csv/usuarios/usuarios.csv")

# Mapeo de códigos de área a nombres legibles
AREAS_NOMBRES = {
    'ciencias_bio': 'Ciencias Biológicas',
    'ciencias_eco': 'Ciencias Económicas',
    'ciencias_exa': 'Ciencias Exactas',
    'ciencias_soc': 'Ciencias Sociales',
    'ed_inst': 'Educación Institucional',
    'ed_lib': 'Educación Libre',
    'human_y_art': 'Humanidades y Artes',
    'ing': 'Ingenierías',
    'multi': 'Multidisciplinarias'
}

CATALOGOS = {
    'conacyt': 'Catálogo CONACYT',
    'jcr': 'Catálogo JCR',
    'mla': 'Catálogo MLA',
    'scielo': 'Catálogo SCIELO',
    'scopus': 'Catálogo SCOPUS'
}


@app.route('/')
def index():
    """Página principal del sistema"""
    return render_template('index.html', 
                         logged_in='email' in session,
                         nombre_usuario=session.get('nombre'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Maneja el inicio de sesión de usuarios"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if sistema.login(email, password):
            session['logged_in'] = True
            session['email'] = email
            session['nombre_completo'] = sistema.current_user.nombre_completo
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('index'))
        
        flash('Credenciales incorrectas', 'danger')
    
    return render_template('login.html', sistema=sistema)

@app.route('/logout')
def logout():
    """Cierra la sesión del usuario"""
    sistema.logout()
    session.clear()
    flash('Sesión cerrada correctamente', 'info')
    return redirect(url_for('index'))

@app.route('/area')
def area():
    """Muestra la página de selección de áreas"""
    return render_template('area.html')

@app.route('/area_detalle/<area>')
def area_detalles(area):
    """Muestra las revistas de un área específica"""
    nombre_area = AREAS_NOMBRES.get(area, area)
    revistas = sistema.obtener_revistas_por_area(area)
    return render_template('area_detalle.html', 
                        area=nombre_area, 
                        revistas=revistas)

@app.route('/explora')
def explora():
    """Página principal de exploración"""
    return render_template('explora.html')

@app.route('/explorar/<letra>')
def explorar(letra):
    """Muestra revistas filtradas por letra inicial"""
    revistas_por_letra = sistema.clasificar_revistas_por_letra(sistema.revistas)
    revistas_filtradas = revistas_por_letra.get(letra.upper(), [])
    
    return render_template('explorar.html',
                        revistas_por_letra=revistas_por_letra,
                        letra_actual=letra.upper(),
                        revistas=revistas_filtradas,
                        logged_in='email' in session,
                        AREAS_NOMBRES=AREAS_NOMBRES)

@app.route('/revista/<int:id_revista>')
def revista(id_revista):
    """Muestra los detalles completos de una revista"""
    revista = sistema.obtener_revista_por_id(id_revista)
    if not revista:
        flash('Revista no encontrada', 'danger')
        return redirect(url_for('index'))
    
    return render_template('revista.html',
                        revista=revista,
                        AREAS_NOMBRES=AREAS_NOMBRES)

@app.route('/catalogos')
def catalogos():
    """Muestra información general sobre los catálogos"""
    return render_template('catalogos.html')

@app.route('/catalogo/<catalogo>')
def catalogo_detalle(catalogo):
    """Muestra revistas de un catálogo específico"""    
    nombre_legible = CATALOGOS.get(catalogo, catalogo)
    revistas = sistema.obtener_revista_por_catalogo(catalogo)
    
    return render_template('catalogo_detalle.html', 
                        catalogo=nombre_legible, 
                        revistas=revistas)

@app.route('/busqueda')
def busqueda():
    """Realiza búsquedas de revistas"""
    query = request.args.get('q', '')
    revistas = sistema.buscar_revistas(query) if query else []
    
    return render_template('busqueda.html',
                        query=query,
                        revistas=revistas,
                        AREAS_NOMBRES=AREAS_NOMBRES)

@app.route('/creditos')
def creditos():
    """Muestra los créditos del sistema"""
    return render_template('creditos.html')

@app.route('/inicio')
def inicio():
    """Página de inicio del sistema"""
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)