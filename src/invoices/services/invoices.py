from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from config.mongodb import mongo
from bson import ObjectId  # Importa la clase ObjectId de bson

@jwt_required()
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
    
    
@jwt_required()
def get_all_invoices():
    id_usuario = get_jwt_identity()
    invoices = mongo.db.invoices.find({'id_usuario': id_usuario})

    if invoices:
        invoices_list = []
        for invoice in invoices:
            invoices_list.append({
                'id_factura': str(invoice['_id']),
                'fecha': invoice['fecha'].strftime('%Y-%m-%d %H:%M:%S'),
                'total': invoice['total'],
                'productos': invoice['productos']
            })
        return jsonify({'invoices': invoices_list}), 200
    else:
        return jsonify({'message': 'No se encontraron facturas para este usuario.'}), 404

        

@jwt_required()
def get_invoice_by_id(invoice_id):
    id_usuario = get_jwt_identity()
    invoice = mongo.db.invoices.find_one({'_id': ObjectId(invoice_id), 'id_usuario': id_usuario})

    if invoice:
        invoice_data = {
            'id_factura': str(invoice['_id']),
            'fecha': invoice['fecha'].strftime('%Y-%m-%d %H:%M:%S'),
            'total': invoice['total'],
            'productos': invoice['productos']
        }
        return jsonify({'invoice': invoice_data}), 200
    else:
        return jsonify({'message': 'No se encontró la factura solicitada para este usuario.'}), 404

@jwt_required()
def delete_invoice(invoice_id):
    try:
        invoice_object_id = ObjectId(invoice_id)
        
        deleted_invoice = mongo.db.invoices.find_one_and_delete({'_id': invoice_object_id})
        
        if deleted_invoice:
            return jsonify({'message': 'Factura eliminada correctamente.'}), 200
        else:
            return jsonify({'message': 'No se encontró la factura con el ID proporcionado.'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@jwt_required()
def update_invoice_by_id(invoice_id):
    id_usuario = get_jwt_identity()
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No se proporcionaron datos para actualizar.'}), 400

    try:
        invoice = mongo.db.invoices.find_one({'_id': ObjectId(invoice_id), 'id_usuario': id_usuario})

        if not invoice:
            return jsonify({'error': 'La factura no existe o no pertenece a este usuario.'}), 404

        mongo.db.invoices.update_one({'_id': ObjectId(invoice_id)}, {'$set': data})

        return jsonify({'message': 'Factura actualizada exitosamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500