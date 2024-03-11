from flask import request
from config.mongodb import mongo

def create_usuario_service():
    data = request.get_json()
    username = data.get('username',None)
    email = data.get('email',None)
    password = data.get('password',None)
    if username:
        response = mongo.db.todos.insert_one({
            'username': username,
            'email': email,
            'password': password,
            'done': False,
        })
        result = {
            'id': str(response.inserted_id),
            'username': username,
            'email': email,
            'password': password,
            'done': False,
    }
        return result
    else:
        return 'invalid payload', 400