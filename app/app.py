from flask import Flask, render_template, request, redirect, url_for, session, flash
from funciones import SistemaRevistas

app = Flask(__name__)
app.secret_key = 'nose'  # Cambiar en producción!

sistema = SistemaRevistas()

@app.route('/')
def index():
    """Página principal del sistema"""
    return render_template('index.html', 
                         logged_in='username' in session,
                         nombre_usuario=session.get('username'))

@app.route("/inicio")
def index_redirect():
    return render_template("index.html")

@app.route("/area")
def area():
    return render_template("area.html")

@app.route("/explorar")
def explorar():
    return render_template("explorar.html")

@app.route("/catalogos")
def catalogos():
    return render_template("catalogos.html")

@app.route("/busqueda")
def busqueda():
    query = request.args.get('q', '')
    return render_template("busqueda.html", query=query)

@app.route("/creditos")
def creditos():
    return render_template("creditos.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Maneja el inicio de sesión"""
    if 'username' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if sistema.login(username, password):
            session['logged_in'] = True
            session['username'] = sistema.usuario_actual.nombre_completo
            session['user_id'] = username
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('index'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Cierra la sesión del usuario"""
    sistema.logout()
    session.clear()
    flash('Has cerrado sesión correctamente', 'info')
    return redirect(url_for('index'))

@app.route('/favoritos')
def favoritos():
    """Muestra las revistas favoritas del usuario"""
    if 'username' not in session:
        flash('Debes iniciar sesión para ver tus favoritos', 'warning')
        return redirect(url_for('login'))
    
    revistas = sistema.obtener_favoritos()
    return render_template('favoritos.html', 
                         revistas=revistas,
                         nombre_usuario=session['username'])

@app.route('/guardar_favorito/<int:revista_id>', methods=['POST'])
def guardar_favorito(revista_id):
    """Guarda o elimina una revista de favoritos"""
    if 'username' not in session:
        return {'success': False, 'message': 'No autenticado'}, 401
    
    # Verificar si la revista existe
    revista = next((r for r in sistema.revistas if r['id'] == revista_id), None)
    if not revista:
        return {'success': False, 'message': 'Revista no encontrada'}, 404
    
    # Alternar estado de favorito
    if revista_id in sistema.usuario_actual.favoritos:
        sistema.eliminar_favorito(revista_id)
        action = 'eliminada'
    else:
        sistema.agregar_favorito(revista_id)
        action = 'añadida'
    
    return {
        'success': True,
        'action': action,
        'message': f'Revista {action} a favoritos'
    }

@app.route('/buscar')
def buscar():
    """Busca revistas por título"""
    query = request.args.get('q', '')
    resultados = sistema.buscar_revistas(query) if query else []
    return render_template('busqueda.html',
                         query=query,
                         revistas=resultados,
                         logged_in='username' in session)

if __name__ == '__main__':
    app.run(debug=True)