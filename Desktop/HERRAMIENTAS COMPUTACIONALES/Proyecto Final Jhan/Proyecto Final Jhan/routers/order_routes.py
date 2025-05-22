from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from controllers.order_controller import (
    obtener_pedidos, obtener_pedido_por_id, crear_pedido, actualizar_estado_pedido
)
from controllers.menu_controller import obtener_platos
from routers.auth_routes import login_required

# Crear el Blueprint
order_bp = Blueprint('order', __name__)

@order_bp.route('/pedidos')
@login_required
def pedidos_list():
    """
    Ruta para listar los pedidos.
    """
    filtro = request.args.get('filtro', '')
    estado = request.args.get('estado')
    fecha = request.args.get('fecha')
    
    pedidos = obtener_pedidos(filtro, estado, fecha)
    
    return render_template('orders.html', 
                          pedidos=pedidos, 
                          filtro=filtro, 
                          estado=estado, 
                          fecha=fecha)

@order_bp.route('/pedidos/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_pedido():
    """
    Ruta para crear un nuevo pedido.
    """
    platos = obtener_platos(disponible=True)
    
    if request.method == 'POST':
        cliente = request.form.get('cliente')
        mesa = request.form.get('mesa')
        
        # Validaciones básicas
        if not cliente:
            flash("El nombre del cliente es obligatorio", "error")
            return render_template('order_form.html', platos=platos)
        
        # Obtener detalles del pedido desde el formulario
        detalles = []
        plato_ids = request.form.getlist('plato_id[]')
        cantidades = request.form.getlist('cantidad[]')
        notas = request.form.getlist('notas[]')
        
        if not plato_ids or len(plato_ids) == 0:
            flash("Debe agregar al menos un plato al pedido", "error")
            return render_template('order_form.html', platos=platos)
        
        for i in range(len(plato_ids)):
            if int(cantidades[i]) > 0:
                detalles.append({
                    'plato_id': int(plato_ids[i]),
                    'cantidad': int(cantidades[i]),
                    'notas': notas[i] if i < len(notas) else ''
                })
        
        if not detalles:
            flash("Debe agregar al menos un plato con cantidad mayor a cero", "error")
            return render_template('order_form.html', platos=platos)
        
        pedido_id = crear_pedido(cliente, mesa, detalles)
        if pedido_id:
            return redirect(url_for('order.pedidos_list'))
    
    return render_template('order_form.html', platos=platos)

@order_bp.route('/pedidos/<int:pedido_id>')
@login_required
def ver_pedido(pedido_id):
    """
    Ruta para ver los detalles de un pedido.
    """
    pedido = obtener_pedido_por_id(pedido_id)
    if not pedido:
        flash("Pedido no encontrado", "error")
        return redirect(url_for('order.pedidos_list'))
    
    return render_template('order_detail.html', pedido=pedido)

@order_bp.route('/pedidos/actualizar-estado/<int:pedido_id>', methods=['POST'])
@login_required
def actualizar_estado(pedido_id):
    """
    Ruta para actualizar el estado de un pedido.
    """
    nuevo_estado = request.form.get('estado')
    
    if actualizar_estado_pedido(pedido_id, nuevo_estado):
        return redirect(url_for('order.ver_pedido', pedido_id=pedido_id))
    
    return redirect(url_for('order.ver_pedido', pedido_id=pedido_id))

@order_bp.route('/api/platos')
@login_required
def api_platos():
    """
    API para obtener platos disponibles en formato JSON.
    """
    platos = obtener_platos(disponible=True)
    return jsonify(platos)