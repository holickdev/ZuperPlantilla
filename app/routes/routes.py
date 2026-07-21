# Este módulo ha sido refactorizado a 'main.py' utilizando el Blueprint 'main_bp'.
# Se mantiene este archivo como referencia histórica.

from app.routes.main import main_bp

def init_routes(app):
    app.register_blueprint(main_bp)