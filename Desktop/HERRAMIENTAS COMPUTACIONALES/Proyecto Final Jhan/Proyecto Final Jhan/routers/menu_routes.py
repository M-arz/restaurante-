from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from controllers.menu_controller import (
    obtener_categorias, obtener_platos, obtener_plato_por_id,
    crear_plato, actualizar_plato, eliminar_plato
)
from routers.auth_routes import login_required
import os
from werkzeug.utils import secure_filename

# Crear el Blueprint
menu_bp = Blueprint('menu', __name__)

# Configuración para subir imágenes
UPLOAD_FOLDER = 'static/uploads/platos'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@menu_bp.route('/dashboard')
@login_required
def dashboard():
    """
    Ruta para el dashboard principal.
    """
    return render_template('dashboard.html')

@menu_bp.route('/menu')
@login_required
def menu_list():
    """
    Ruta para listar los platos del menú.
    """
    filtro = request.args.get('filtro', '')
    categoria_id = request.args.get('categoria_id', type=int)
    
    categorias = obtener_categorias()
    platos = obtener_platos(filtro, categoria_id)
    
    return render_template('menu.html', 
                          platos=platos, 
                          categorias=categorias, 
                          filtro=filtro, 
                          categoria_id=categoria_id)

@menu_bp.route('/menu/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_plato():
    """
    Ruta para crear un nuevo plato.
    """
    categorias = obtener_categorias()
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        precio = request.form.get('precio')
        categoria_id = request.form.get('categoria_id')
        disponible = 'disponible' in request.form
        
        # Validaciones básicas
        if not nombre or not precio or not categoria_id:
            flash("Los campos nombre, precio y categoría son obligatorios", "error")
            return render_template('menu_form.html', categorias=categorias)
        
        # Manejar la imagen si se proporciona
        imagen_path = None
        if 'imagen' in request.files:
            file = request.files['imagen']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Crear directorio si no existe
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(file_path)
                imagen_path = file_path
        
        if crear_plato(nombre, descripcion, precio, categoria_id, disponible, imagen_path):
            return redirect(url_for('menu.menu_list'))
    
    return render_template('menu_form.html', categorias=categorias, plato=None)

@menu_bp.route('/menu/editar/<int:plato_id>', methods=['GET', 'POST'])
@login_required
def editar_plato(plato_id):
    """
    Ruta para editar un plato existente.
    """
    plato = obtener_plato_por_id(plato_id)
    if not plato:
        flash("Plato no encontrado", "error")
        return redirect(url_for('menu.menu_list'))
    
    categorias = obtener_categorias()
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        precio = request.form.get('precio')
        categoria_id = request.form.get('categoria_id')
        disponible = 'disponible' in request.form
        
        # Validaciones básicas
        if not nombre or not precio or not categoria_id:
            flash("Los campos nombre, precio y categoría son obligatorios", "error")
            return render_template('menu_form.html', categorias=categorias, plato=plato)
        
        # Manejar la imagen si se proporciona
        imagen_path = plato['imagen']  # Mantener la imagen actual por defecto
        if 'imagen' in request.files:
            file = request.files['imagen']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Crear directorio si no existe
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(file_path)
                imagen_path = file_path
        
        if actualizar_plato(plato_id, nombre, descripcion, precio, categoria_id, disponible, imagen_path):
            return redirect(url_for('menu.menu_list'))
    
    return render_template('menu_form.html', categorias=categorias, plato=plato)

@menu_bp.route('/menu/eliminar/<int:plato_id>', methods=['POST'])
@login_required
def borrar_plato(plato_id):
    """
    Ruta para eliminar un plato.
    """
    if eliminar_plato(plato_id):
        return redirect(url_for('menu.menu_list'))
    return redirect(url_for('menu.menu_list'))