from werkzeug.security import generate_password_hash, check_password_hash
from flask import session, flash, redirect, url_for
from conexion.db import get_db

def registrar_usuario(nombre, email, password):
    """
    Registra un nuevo usuario administrador en el sistema.
    
    Args:
        nombre: Nombre completo del usuario
        email: Correo electrónico (será el usuario para iniciar sesión)
        password: Contraseña del usuario
    
    Returns:
        bool: True si el registro fue exitoso, False en caso contrario
    """
    db = get_db()
    cursor = db.cursor()
    
    try:
        # Verificar si el email ya existe
        cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
        if cursor.fetchone():
            flash("El correo electrónico ya está registrado", "error")
            return False
        
        # Encriptar la contraseña
        password_hash = generate_password_hash(password)
        
        # Insertar el nuevo usuario
        cursor.execute(
            "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
            (nombre, email, password_hash)
        )
        db.commit()
        flash("Usuario registrado correctamente", "success")
        return True
    
    except Exception as e:
        db.rollback()
        flash(f"Error al registrar usuario: {str(e)}", "error")
        return False

def iniciar_sesion(email, password):
    """
    Valida las credenciales del usuario e inicia sesión.
    
    Args:
        email: Correo electrónico del usuario
        password: Contraseña del usuario
    
    Returns:
        bool: True si el inicio de sesión fue exitoso, False en caso contrario
    """
    db = get_db()
    cursor = db.cursor()
    
    try:
        # Buscar usuario por email
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        usuario = cursor.fetchone()
        
        if not usuario or not check_password_hash(usuario['password'], password):
            flash("Credenciales incorrectas", "error")
            return False
        
        # Guardar información de sesión
        session['usuario_id'] = usuario['id']
        session['usuario_nombre'] = usuario['nombre']
        session['usuario_email'] = usuario['email']
        
        flash(f"Bienvenido, {usuario['nombre']}", "success")
        return True
    
    except Exception as e:
        flash(f"Error al iniciar sesión: {str(e)}", "error")
        return False

def cerrar_sesion():
    """
    Cierra la sesión del usuario actual.
    """
    session.clear()
    flash("Has cerrado sesión correctamente", "info")
    return redirect(url_for('auth.login'))

def usuario_actual():
    """
    Obtiene la información del usuario actual.
    
    Returns:
        dict: Información del usuario o None si no hay sesión
    """
    if 'usuario_id' in session:
        return {
            'id': session['usuario_id'],
            'nombre': session['usuario_nombre'],
            'email': session['usuario_email']
        }
    return None