from flask import Flask, redirect, url_for
from routers.auth_routes import auth_bp
from routers.menu_routes import menu_bp
from routers.order_routes import order_bp
from conexion.db import init_app
import os

def create_app():
    """
    Función para crear y configurar la aplicación Flask.
    """
    app = Flask(__name__)
    
    # Configuración
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'clave_secreta_por_defecto')
    app.config['UPLOAD_FOLDER'] = 'static/uploads'
    
    # Inicializar la conexión a la base de datos
    init_app(app)
    
    # Registrar blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(menu_bp)
    app.register_blueprint(order_bp)
    
    # Ruta principal
    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))
    
    return app