from flask import request
from config.mongodb import mongo

def create_invoice_service():
    data = request.get_json()
    title = data.get('title',None)
    description = data.get('description',None)
    if title:
        response = mongo.db.todos.insert_one({
            'title': title,
            'description': description,
            'done': False,
        })
        result = {
            'id': str(response.inserted_id),
            'title': title,
            'description': description,
            'done': False,
    }
        return result
    else:
        return 'invalid payload', 400