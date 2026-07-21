import os
from flask import Flask
from dotenv import load_dotenv

def create_app():
    """
    Función App Factory para inicializar y configurar la aplicación Flask.
    """
    # Carga las variables de entorno definidas en el archivo .env
    load_dotenv()
    
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "default_secret_key")

    # Registro del Blueprint principal que contiene las rutas de la aplicación
    from app.routes.main import main_bp
    app.register_blueprint(main_bp)
    
    return app