from flask import Flask, render_template, request, redirect, url_for, session, flash
from funciones import SistemaRevistas  # Asegúrate de que la clase Revistas esté definida aquí
import os # Asegúrate de que la clase RevistaManager esté definida aquí

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY') or 'tu-clave-secreta-aqui'

# Inicializa el sistema
sistema = SistemaRevistas()
sistema.cargar_datos("datos/json/revistas_info_parte_1.json", "datos/csv/areas")


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


@app.route('/revista/<int:id_revista>')
def mostrar_revista(id_revista):
    revista = sistema.obtener_revista_por_id(id_revista)
    if revista:
        return render_template('revista.html', revista=revista)
    else:
        return "Revista no encontrada", 404




@app.route('/explorar')
def explorar():
    """Muestra revistas por área"""
    area = request.args.get('area', '')
    if not area:
        return redirect(url_for('area'))
    
    area_nombre = sistema.AREAS.get(area, area)
    revistas = sistema.obtener_revistas_por_area(area)  # Método de la clase Revistas
    
    return render_template('explorar.html',
                         area=area_nombre,
                         revistas=revistas,
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
    
    return render_template('revista.html',
                         revista=revista,
                         es_favorito=es_favorito,
                         logged_in='username' in session)

@app.route('/catalogos')
def catalogos():
    """Muestra información sobre los catálogos"""
    return render_template('catalogos.html')

@app.route('/creditos')
def creditos():
    """Muestra los créditos del sistema"""
    return render_template('creditos.html')

@app.route('/busqueda')
def busqueda():
    """Realiza búsqueda de revistas"""
    query = request.args.get('q', '')
    resultados = sistema.buscar_revistas(query) if query else []  # Método de búsqueda de la clase Revistas
    return render_template('busqueda.html',
                         query=query,
                         revistas=resultados,
                         logged_in='username' in session)

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
