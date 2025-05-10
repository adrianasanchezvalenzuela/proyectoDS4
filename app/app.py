from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

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

@app.route("/buscar")
def buscar():
    query = request.args.get('q', '')
    return render_template("busqueda.html", query=query)

@app.route("/busqueda")
def busqueda():
    query = request.args.get('q', '')
    return render_template("busqueda.html", query=query)

@app.route("/creditos")
def creditos():
    return render_template("creditos.html")

@app.route("/login")
def login():
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)