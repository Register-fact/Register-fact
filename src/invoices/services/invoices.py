from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from config.mongodb import mongo

@jwt_required()  # Requiere autenticación JWT
def addInvoice():
    data = request.get_json()
    id_usuario = get_jwt_identity()

    # Validar los datos recibidos
    if 'productos' not in data:
        return jsonify({'error': 'La lista de productos es obligatoria.'}), 400

    suma_total = 0
    for producto in  data['productos']:
        precio_unitario = producto["precio_unitario"]
        cantidad = producto["cantidad"]
        precio_total_producto = precio_unitario * cantidad
    
        suma_total += precio_total_producto
    try:
        factura = {
            'id_usuario': id_usuario,
            'fecha': datetime.utcnow(),  # Fecha actual
            'productos': data['productos'],
            'total': suma_total
        }
        factura_insertada = mongo.db.invoices.insert_one(factura)
        factura_id = str(factura_insertada.inserted_id)
        return jsonify({'message': 'Factura registrada exitosamente', 'factura_id': factura_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500