from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.services.user_service import verify_credentials, register_user

# Definición del Blueprint principal para agrupar todas las rutas del proyecto
main_bp = Blueprint("main", __name__)


def login_required(f):
    """
    Decorador personalizado para proteger rutas que requieren autenticación.
    Si el id del usuario no existe en la sesión, redirige al inicio de sesión.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("main.login"))
        return f(*args, **kwargs)
    return decorated_function


@main_bp.route("/")
def index():
    """Ruta principal / página de bienvenida."""
    return render_template("index.html")


@main_bp.route("/login", methods=["GET", "POST"])
def login():
    """Maneja la vista de login (GET) y el procesamiento de inicio de sesión (POST)."""
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        user = verify_credentials(email, password)
        
        if user:
            # Guarda el ID del usuario en la sesión HTTP
            session["user_id"] = user["id"]
            return redirect(url_for("main.dashboard"))
        
        flash("Credenciales incorrectas", "error")
        return redirect(url_for("main.login"))
        
    return render_template("login.html")


@main_bp.route("/sign-up", methods=["GET", "POST"])
def signup():
    """Maneja la vista de registro (GET) y la creación de un nuevo usuario (POST)."""
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        success = register_user(email, password)
        
        if success:
            flash("Usuario registrado exitosamente. Por favor inicia sesión.", "success")
            return redirect(url_for("main.login"))
        
        flash("El correo electrónico ya está registrado.", "error")
        return redirect(url_for("main.signup"))
        
    return render_template("sign-up.html")


@main_bp.route("/dashboard")
@login_required
def dashboard():
    """Vista protegida del panel principal del usuario."""
    return render_template("dashboard.html")


@main_bp.route("/logout")
def logout():
    """Cierra la sesión del usuario eliminando los datos de la sesión."""
    session.clear()
    return redirect(url_for("main.index"))
