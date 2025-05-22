from conexion.db import get_db
from flask import flash


def obtener_categorias():
    """
    Obtiene todas las categorías de platos.
    
    Returns:
        list: Lista de categorías
    """
    db = get_db()
    cursor = db.cursor()
    
    try:
        cursor.execute("SELECT * FROM categorias ORDER BY nombre")
        return cursor.fetchall()
    except Exception as e:
        flash(f"Error al obtener categorías: {str(e)}", "error")
        return []

def obtener_platos(filtro=None, categoria_id=None, disponible=None):
    """
    Obtiene los platos del menú con filtros opcionales.
    
    Args:
        filtro: Texto para filtrar por nombre o descripción
        categoria_id: ID de la categoría para filtrar
        disponible: Si es True, solo muestra platos disponibles; si es False, solo no disponibles; si es None, muestra todos
    
    Returns:
        list: Lista de platos que cumplen con los filtros
    """
    db = get_db()
    cursor = db.cursor()
    
    query = """
        SELECT p.*, c.nombre as categoria_nombre 
        FROM platos p
        LEFT JOIN categorias c ON p.categoria_id = c.id
        WHERE 1=1
    """
    params = []
    
    if filtro:
        query += " AND (p.nombre LIKE %s OR p.descripcion LIKE %s)"
        params.extend([f"%{filtro}%", f"%{filtro}%"])
    
    if categoria_id:
        query += " AND p.categoria_id = %s"
        params.append(categoria_id)
    
    if disponible is not None:
        query += " AND p.disponible = %s"
        params.append(disponible)
    
    query += " ORDER BY p.nombre"
    
    try:
        cursor.execute(query, params)
        return cursor.fetchall()
    except Exception as e:
        flash(f"Error al obtener platos: {str(e)}", "error")
        return []

def obtener_plato_por_id(plato_id):
    """
    Obtiene un plato específico por su ID.
    
    Args:
        plato_id: ID del plato a obtener
    
    Returns:
        dict: Información del plato o None si no existe
    """
    db = get_db()
    cursor = db.cursor()
    
    try:
        cursor.execute("""
            SELECT p.*, c.nombre as categoria_nombre 
            FROM platos p
            LEFT JOIN categorias c ON p.categoria_id = c.id
            WHERE p.id = %s
        """, (plato_id,))
        return cursor.fetchone()
    except Exception as e:
        flash(f"Error al obtener plato: {str(e)}", "error")
        return None

def crear_plato(nombre, descripcion, precio, categoria_id, disponible=True, imagen=None):
    """
    Crea un nuevo plato en el menú.
    
    Args:
        nombre: Nombre del plato
        descripcion: Descripción del plato
        precio: Precio del plato
        categoria_id: ID de la categoría
        disponible: Si el plato está disponible
        imagen: Ruta de la imagen del plato
    
    Returns:
        bool: True si la creación fue exitosa, False en caso contrario
    """
    db = get_db()
    cursor = db.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO platos (nombre, descripcion, precio, categoria_id, disponible, imagen)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nombre, descripcion, precio, categoria_id, disponible, imagen))
        db.commit()
        flash("Plato creado correctamente", "success")
        return True
    except Exception as e:
        db.rollback()
        flash(f"Error al crear plato: {str(e)}", "error")
        return False

def actualizar_plato(plato_id, nombre, descripcion, precio, categoria_id, disponible, imagen=None):
    """
    Actualiza la información de un plato existente.
    
    Args:
        plato_id: ID del plato a actualizar
        nombre: Nuevo nombre del plato
        descripcion: Nueva descripción del plato
        precio: Nuevo precio del plato
        categoria_id: Nueva categoría del plato
        disponible: Si el plato está disponible
        imagen: Nueva ruta de la imagen del plato
    
    Returns:
        bool: True si la actualización fue exitosa, False en caso contrario
    """
    db = get_db()
    cursor = db.cursor()
    
    try:
        # Si no se proporciona una nueva imagen, mantener la existente
        if imagen:
            cursor.execute("""
                UPDATE platos 
                SET nombre = %s, descripcion = %s, precio = %s, 
                    categoria_id = %s, disponible = %s, imagen = %s
                WHERE id = %s
            """, (nombre, descripcion, precio, categoria_id, disponible, imagen, plato_id))
        else:
            cursor.execute("""
                UPDATE platos 
                SET nombre = %s, descripcion = %s, precio = %s, 
                    categoria_id = %s, disponible = %s
                WHERE id = %s
            """, (nombre, descripcion, precio, categoria_id, disponible, plato_id))
        
        db.commit()
        flash("Plato actualizado correctamente", "success")
        return True
    except Exception as e:
        db.rollback()
        flash(f"Error al actualizar plato: {str(e)}", "error")
        return False

def eliminar_plato(plato_id):
    """
    Elimina un plato del menú.
    
    Args:
        plato_id: ID del plato a eliminar
    
    Returns:
        bool: True si la eliminación fue exitosa, False en caso contrario
    """
    db = get_db()
    cursor = db.cursor()
    
    try:
        # Verificar si el plato está en algún pedido
        cursor.execute("SELECT COUNT(*) as count FROM detalles_pedido WHERE plato_id = %s", (plato_id,))
        result = cursor.fetchone()
        
        if result['count'] > 0:
            flash("No se puede eliminar el plato porque está asociado a pedidos", "error")
            return False
        
        cursor.execute("DELETE FROM platos WHERE id = %s", (plato_id,))
        db.commit()
        flash("Plato eliminado correctamente", "success")
        return True
    except Exception as e:
        db.rollback()
        flash(f"Error al eliminar plato: {str(e)}", "error")
        return False