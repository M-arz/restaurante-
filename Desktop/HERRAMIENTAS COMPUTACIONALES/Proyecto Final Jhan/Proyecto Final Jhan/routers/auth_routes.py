from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from controllers.auth_controller import registrar_usuario, iniciar_sesion, cerrar_sesion, usuario_actual
from functools import wraps

# Crear el Blueprint
auth_bp = Blueprint('auth', __name__)

# Decorador para verificar si el usuario ha iniciado sesión
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            flash("Debes iniciar sesión para acceder a esta página", "error")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Ruta para el inicio de sesión.
    """
    # Si el usuario ya está autenticado, redirigir al dashboard
    if 'usuario_id' in session:
        return redirect(url_for('menu.dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if iniciar_sesion(email, password):
            return redirect(url_for('menu.dashboard'))
    
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Ruta para el registro de nuevos usuarios.
    """
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validaciones básicas
        if not nombre or not email or not password:
            flash("Todos los campos son obligatorios", "error")
        elif password != confirm_password:
            flash("Las contraseñas no coinciden", "error")
        elif len(password) < 6:
            flash("La contraseña debe tener al menos 6 caracteres", "error")
        else:
            if registrar_usuario(nombre, email, password):
                flash("Usuario registrado correctamente. Ahora puedes iniciar sesión", "success")
                return redirect(url_for('auth.login'))
    
    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    """
    Ruta para cerrar sesión.
    """
    return cerrar_sesion()