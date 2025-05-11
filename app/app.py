from flask import Flask, render_template, request, redirect, url_for, session, flash
from funciones import SistemaRevistas  
import os 

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY') or 'tu-clave-secreta-aqui'

# Inicializa el sistema
sistema = SistemaRevistas()
sistema.cargar_datos("datos/json/revistas_info_parte_1.json", "datos/csv/areas", "datos/csv/catalogos")


@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html', 
                         logged_in='username' in session,
                         nombre_usuario=session.get('nombre_completo'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Maneja el inicio de sesión"""
    if 'username' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if sistema.login(username, password):  # Aquí se usa el método login de la clase Revistas
            session['logged_in'] = True
            session['username'] = username
            session['nombre_completo'] = sistema.usuario_actual.nombre_completo
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('index'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
    
    return render_template('login.html')

@app.route('/inicio')
def inicio():
    """Redirige a la página de inicio"""
    return redirect(url_for('index'))
    
@app.route('/logout')
def logout():
    """Cierra la sesión del usuario"""
    sistema.logout()  # Usamos el método logout de la clase Revistas
    session.clear()
    flash('Has cerrado sesión correctamente', 'info')
    return redirect(url_for('index'))

@app.route('/area')
def area():
    return render_template('area.html')


@app.route('/area_detalle/<area>')
def area_detalles(area):
    AREAS = {
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

    # Obtener nombre legible del área
    nombre_area_legible = AREAS.get(area, area)  # Usa el nombre legible si existe, si no, deja el código

    # Obtener las revistas del área usando el sistema ya cargado
    revistas = sistema.obtener_revistas_por_area(area)

    # Pasar las revistas y el nombre legible del área a la plantilla
    return render_template('area_detalle.html', area=nombre_area_legible, revistas=revistas)


@app.route('/explora')
def explora():
    return render_template('explora.html')

@app.route('/explorar/<letra>')
def explorar(letra):
    """Muestra todas las revistas clasificadas por la primera letra de su título o las filtradas por la letra seleccionada."""
    # Clasificar las revistas por la primera letra de su título
    revistas_por_letra = sistema.clasificar_revistas_por_letra(sistema.revistas)

    # Si se selecciona una letra, filtrar las revistas por esa letra
    if letra:
        revistas_filtradas = revistas_por_letra.get(letra.upper(), [])
        return render_template('explorar.html',
                               revistas_por_letra=revistas_por_letra,
                               letra_actual=letra.upper(),
                               revistas=revistas_filtradas,
                               logged_in='username' in session)
    else:
        # Si no hay letra, mostrar todas las revistas clasificadas por letra
        return render_template('explorar.html',
                               revistas_por_letra=revistas_por_letra,
                               logged_in='username' in session)





@app.route('/revista/<int:id_revista>')
def revista(id_revista):
    """Muestra detalles de una revista"""
    revista = sistema.obtener_revista_por_id(id_revista)  # Método de la clase Revistas
    if not revista:
        flash('Revista no encontrada', 'danger')
        return redirect(url_for('index'))
    
    es_favorito = False
    if 'username' in session and sistema.usuario_actual:
        es_favorito = id_revista in sistema.usuario_actual.favoritos
    
    print(f"Catálogo: {revista.catalogo}") 
    print(f"Área: {revista.seccion}")
    return render_template('revista.html',
                         revista=revista,
                         es_favorito=es_favorito,
                         logged_in='username' in session)

@app.route('/catalogos')
def catalogos():
    """Muestra información sobre los catálogos"""
    return render_template('catalogos.html')

@app.route('/catalogo/<catalogo>')
def catalogo_detalle(catalogo):
    CATALOGOS = {
        'conacyt': 'Catálogo CONACYT',
        'jcr': 'Catálogo JCR',
        'mla': 'Catálogo MLA',
        'scielo': 'Catálogo SCIELO',
        'scopus': 'Catálogo SCOPUS'
    }

    # Obtener nombre legible del catálogo
    nombre_legible = CATALOGOS.get(catalogo, catalogo)

    # Obtener las revistas por catálogo usando el sistema
    revistas = sistema.obtener_revista_por_catalogo(catalogo)

    return render_template('catalogo_detalle.html', catalogo=nombre_legible, revistas=revistas)



@app.route('/creditos')
def creditos():
    """Muestra los créditos del sistema"""
    return render_template('creditos.html')

@app.route('/busqueda')
def busqueda():
    query = request.args.get('q', '')
    if query:
        revistas = sistema.buscar_revistas(query)
    else:
        revistas = []

    return render_template('busqueda.html', query=query, revistas=revistas)


@app.route('/favoritos')
def favoritos():
    """Muestra las revistas favoritas del usuario"""
    if 'username' not in session:
        flash('Debes iniciar sesión para ver tus favoritos', 'warning')
        return redirect(url_for('login'))
    
    revistas = sistema.obtener_favoritos()  # Método para obtener favoritos
    return render_template('favoritos.html',
                         revistas=revistas,
                         logged_in=True)

@app.route('/toggle_favorito/<int:id_revista>', methods=['POST'])
def toggle_favorito(id_revista):
    """Agrega o elimina una revista de favoritos"""
    if 'username' not in session:
        return {'success': False, 'message': 'No autenticado'}, 401
    
    if id_revista not in sistema.revistas:
        return {'success': False, 'message': 'Revista no encontrada'}, 404
    
    if id_revista in sistema.usuario_actual.favoritos:
        sistema.eliminar_favorito(id_revista)  # Método de eliminar favorito de la clase Revistas
        action = 'eliminada'
    else:
        sistema.agregar_favorito(id_revista)  # Método de agregar favorito de la clase Revistas
        action = 'añadida'
    
    return {
        'success': True,
        'action': action,
        'message': f'Revista {action} a favoritos'
    }

if __name__ == '__main__':
    app.run(debug=True)
