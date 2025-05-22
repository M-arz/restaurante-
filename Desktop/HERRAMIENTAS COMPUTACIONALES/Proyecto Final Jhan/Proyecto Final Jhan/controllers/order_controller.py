from conexion.db import get_db
from flask import flash
import datetime

def obtener_pedidos(filtro=None, estado=None, fecha=None):
    """
    Obtiene los pedidos con filtros opcionales.
    
    Args:
        filtro: Texto para filtrar por cliente o mesa
        estado: Estado del pedido para filtrar
        fecha: Fecha para filtrar pedidos
    
    Returns:
        list: Lista de pedidos que cumplen con los filtros
    """
    db = get_db()
    cursor = db.cursor()
    
    query = "SELECT * FROM pedidos WHERE 1=1"
    params = []
    
    if filtro:
        query += " AND (cliente LIKE %s OR mesa = %s)"
        params.extend([f"%{filtro}%", filtro if filtro.isdigit() else 0])
    
    if estado:
        query += " AND estado = %s"
        params.append(estado)
    
    if fecha:
        query += " AND DATE(fecha_hora) = %s"
        params.append(fecha)
    
    query += " ORDER BY fecha_hora DESC"
    
    try:
        cursor.execute(query, params)
        pedidos = cursor.fetchall()
        
        # Obtener detalles para cada pedido
        for pedido in pedidos:
            pedido['detalles'] = obtener_detalles_pedido(pedido['id'])
        
        return pedidos
    except Exception as e:
        flash(f"Error al obtener pedidos: {str(e)}", "error")
        return []

def obtener_pedido_por_id(pedido_id):
    """
    Obtiene un pedido específico por su ID.
    
    Args:
        pedido_id: ID del pedido a obtener
    
    Returns:
        dict: Información del pedido o None si no existe
    """
    db = get_db()
    cursor = db.cursor()
    
    try:
        cursor.execute("SELECT * FROM pedidos WHERE id = %s", (pedido_id,))
        pedido = cursor.fetchone()
        
        if pedido:
            pedido['detalles'] = obtener_detalles_pedido(pedido_id)
        
        return pedido
    except Exception as e:
        flash(f"Error al obtener pedido: {str(e)}", "error")
        return None

def obtener_detalles_pedido(pedido_id):
    """
    Obtiene los detalles de un pedido específico.
    
    Args:
        pedido_id: ID del pedido
    
    Returns:
        list: Lista de detalles del pedido
    """
    db = get_db()
    cursor = db.cursor()
    
    try:
        cursor.execute("""
            SELECT d.*, p.nombre as plato_nombre 
            FROM detalles_pedido d
            JOIN platos p ON d.plato_id = p.id
            WHERE d.pedido_id = %s
        """, (pedido_id,))
        return cursor.fetchall()
    except Exception as e:
        flash(f"Error al obtener detalles del pedido: {str(e)}", "error")
        return []

def crear_pedido(cliente, mesa, detalles):
    """
    Crea un nuevo pedido con sus detalles.
    
    Args:
        cliente: Nombre del cliente
        mesa: Número de mesa
        detalles: Lista de detalles del pedido (plato_id, cantidad, notas)
    
    Returns:
        int: ID del pedido creado o None si hubo un error
    """
    db = get_db()
    cursor = db.cursor()
    
    try:
        # Calcular el total del pedido
        total = 0
        for detalle in detalles:
            # Obtener precio del plato
            cursor.execute("SELECT precio FROM platos WHERE id = %s", (detalle['plato_id'],))
            plato = cursor.fetchone()
            if not plato:
                flash(f"El plato con ID {detalle['plato_id']} no existe", "error")
                return None
            
            precio = plato['precio']
            total += precio * detalle['cantidad']
        
        # Crear el pedido
        cursor.execute("""
            INSERT INTO pedidos (cliente, mesa, total, estado)
            VALUES (%s, %s, %s, 'pendiente')
        """, (cliente, mesa, total))
        
        pedido_id = cursor.lastrowid
        
        # Crear los detalles del pedido
        for detalle in detalles:
            cursor.execute("SELECT precio FROM platos WHERE id = %s", (detalle['plato_id'],))
            plato = cursor.fetchone()
            precio = plato['precio']
            
            cursor.execute("""
                INSERT INTO detalles_pedido (pedido_id, plato_id, cantidad, precio_unitario, notas)
                VALUES (%s, %s, %s, %s, %s)
            """, (pedido_id, detalle['plato_id'], detalle['cantidad'], precio, detalle.get('notas', '')))
        
        db.commit()
        flash("Pedido creado correctamente", "success")
        return pedido_id
    except Exception as e:
        db.rollback()
        flash(f"Error al crear pedido: {str(e)}", "error")
        return None

def actualizar_estado_pedido(pedido_id, nuevo_estado):
    """
    Actualiza el estado de un pedido.
    
    Args:
        pedido_id: ID del pedido a actualizar
        nuevo_estado: Nuevo estado del pedido
    
    Returns:
        bool: True si la actualización fue exitosa, False en caso contrario
    """
    db = get_db()
    cursor = db.cursor()
    
    estados_validos = ['pendiente', 'preparando', 'servido', 'pagado']
    if nuevo_estado not in estados_validos:
        flash(f"Estado no válido. Debe ser uno de: {', '.join(estados_validos)}", "error")
        return False
    
    try:
        cursor.execute("UPDATE pedidos SET estado = %s WHERE id = %s", (nuevo_estado, pedido_id))
        db.commit()
        flash("Estado del pedido actualizado correctamente", "success")
        return True
    except Exception as e:
        db.rollback()
        flash(f"Error al actualizar estado del pedido: {str(e)}", "error")
        return False