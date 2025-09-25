from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "clave_secreta"

# Usuarios registrados (simulación en memoria)
usuarios = {}

@app.route("/")
def home():
    if "usuario" in session:
        return redirect(url_for("inicio"))
    return redirect(url_for("login"))

# ------------------ REGISTRO ------------------
@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        usuario = request.form["usuario"]
        password = request.form["password"]
        color = request.form["color"]

        if usuario in usuarios:
            flash("El usuario ya existe. Intenta con otro.", "error")
        else:
            usuarios[usuario] = {"password": password, "color": color}
            flash("Usuario registrado exitosamente.", "success")
            return redirect(url_for("login"))

    return render_template("registro.html")

# ------------------ LOGIN ------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        password = request.form["password"]

        # Caso admin
        if usuario == "admin" and password == "12345678":
            session["usuario"] = "admin"
            session["color"] = "#87CEEB"  # Azul cielo
            return redirect(url_for("inicio"))

        # Caso usuario registrado
        if usuario in usuarios and usuarios[usuario]["password"] == password:
            session["usuario"] = usuario
            session["color"] = usuarios[usuario]["color"]
            return redirect(url_for("inicio"))

        # Caso error
        flash("Credenciales inválidas. Intenta de nuevo.", "error")

    return render_template("login.html")

# ------------------ INICIO ------------------
@app.route("/inicio")
def inicio():
    if "usuario" not in session:
        return redirect(url_for("login"))
    return render_template("inicio.html", usuario=session["usuario"])

# ------------------ LOGOUT ------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
