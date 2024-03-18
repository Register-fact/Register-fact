from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from bson import ObjectId  
from config.mongodb import mongo

from invoices.validations.validJson import schema
from cerberus import Validator

@jwt_required()
def addInvoices():
    validator = Validator(schema)
    data = request.get_json()
    if validator.validate(data):
        lugar_compra = data.get('lugar_compra')
        productos = data.get('productos')
                
        for producto in productos:
            producto['precio_total_unidad'] = producto['cantidad'] * producto['precio_unitario']
        total = sum(producto['cantidad'] * producto['precio_unitario'] for producto in productos)

        user_id = get_jwt_identity()
        current_datetime = datetime.utcnow()
        
        try:
            factura = {
                'id_usuario': user_id,
                'fecha': current_datetime,
                'lugar_compra': lugar_compra,
                'productos': productos,
                'total': total
            }
            factura_insertada = mongo.db.invoices.insert_one(factura)
            factura_id = str(factura_insertada.inserted_id)
            return jsonify({'message': 'Factura registrada exitosamente', 'factura_id': factura_id}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': validator.errors}), 400


        
        
@jwt_required()
def get_all_invoices():
    id_usuario = get_jwt_identity()
    invoices = mongo.db.invoices.find({'id_usuario': id_usuario})

    if invoices:
        invoices_list = []
        for invoice in invoices:
            invoices_list.append({
                'id_factura': str(invoice['_id']),
                'id_usuario': invoice['id_usuario'],
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
            'id_usuario': invoice['id_usuario'],
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
        id_usuario = get_jwt_identity()
        invoice_object_id = ObjectId(invoice_id)
        
        invoice = mongo.db.invoices.find_one({'_id': invoice_object_id})
        if not invoice:
            return jsonify({'error': 'No se encontró la factura con el ID proporcionado'}), 404
        
        if invoice['id_usuario'] != id_usuario:
            return jsonify({'error': 'No tiene permiso para eliminar esta factura'}), 401
        
        deleted_invoice = mongo.db.invoices.find_one_and_delete({'_id': invoice_object_id})
        
        if deleted_invoice:
            return jsonify({'message': 'Factura eliminada correctamente.'}), 200 
           
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Ocurrió un error inesperado'}), 500
    
    
@jwt_required()
def update_invoice_by_id(invoice_id):
    validator = Validator(schema)    
    id_usuario = get_jwt_identity()
    data = request.get_json()

    if validator.validate(data):
        try:
            invoice = mongo.db.invoices.find_one({'_id': ObjectId(invoice_id), 'id_usuario': id_usuario})

            if not invoice:
                return jsonify({'error': 'La factura no existe o no pertenece a este usuario.'}), 404
            
            total = 0
            for producto in data.get('productos', []):
                if 'cantidad' in producto:
                    producto['precio_total_unidad'] = producto['cantidad'] * producto['precio_unitario']
                    total += producto['precio_total_unidad']
            
            data['total'] = total
            
            # Actualiza la factura en la base de datos
            mongo.db.invoices.update_one({'_id': ObjectId(invoice_id)}, {'$set': data})

            return jsonify({'message': 'Factura actualizada exitosamente'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': validator.errors}), 400