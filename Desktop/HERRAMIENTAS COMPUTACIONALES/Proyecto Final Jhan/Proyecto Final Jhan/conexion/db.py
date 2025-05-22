import pymysql
from flask import g

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Cambiar según configuración local
    'db': 'restaurante_db',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def get_db():
    """
    Función para obtener una conexión a la base de datos.
    Si ya existe una conexión en el contexto actual, la reutiliza.
    """
    if 'db' not in g:
        g.db = pymysql.connect(**DB_CONFIG)
    return g.db

def close_db(e=None):
    """
    Cierra la conexión a la base de datos si existe.
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_app(app):
    """
    Registra la función de cierre de la base de datos con la aplicación Flask.
    """
    app.teardown_appcontext(close_db)