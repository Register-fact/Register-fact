from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, unset_jwt_cookies
from flask_bcrypt import Bcrypt, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, jwt_manager, get_jwt
from datetime import datetime 
from config.mongodb import mongo
from auth.validation.ValidationForm import RegistrationForm


bcrypt = Bcrypt()


def create_usuario_service():
    data = request.get_json()
    form = RegistrationForm(data=data)
    
    print(form.username.data)
            
    if  request.method == 'POST' and form.validate():
        username = form.username.data
        email = form.email.data
        password = form.password.data
    
        existing_user = mongo.db.usuarios.find_one({'email': email})
        if existing_user:
            return jsonify({'error': 'El correo electrónico ya está en uso.'}), 400

        current_datetime = datetime.utcnow()
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    
        response = mongo.db.usuarios.insert_one({
            'username': username,
            'email': email,
            'password': hashed_password,
            'created_at': current_datetime,
        })
        result = {
            'id': str(response.inserted_id),
            'username': username,
            'email': email,
            'password': hashed_password,
            'created_at': current_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            'ok': True
    }
        return jsonify(result), 201
    else:
        errors = form.errors
        return jsonify(errors), 400
    

def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    
    user = mongo.db.usuarios.find_one({'username': username})
    
    if not user:
        return jsonify({"msg": "Bad username or password"}), 401
    
    # Verificar la contraseña cifrada
    if not check_password_hash(user['password'], password):
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

@jwt_required()
def logout():
    # Eliminar el token del cliente (eliminar cookies en este caso)
    resp = jsonify({'logout': True})
    unset_jwt_cookies(resp)
    return resp

@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200