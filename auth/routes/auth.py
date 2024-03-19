from flask import Blueprint
from auth.services.usuarios import create_usuario_service, protected, login, logout, refresh_token

usuarios = Blueprint('usuarios', __name__)

@usuarios.route('/protected', methods=['GET'])
def getUsuario():
    return protected()

@usuarios.route('/register', methods=['POST'])
def CreateUsuario():
    return create_usuario_service()

@usuarios.route('/login', methods=['POST'])
def SignIn():
    return login() 

@usuarios.route('/<id>', methods=['GET'])
def getById(id):
    return 'getById'

@usuarios.route('/<id>', methods=['PUT'])
def UpdateUsuario(id):
    return 'UpdateUsuario'

@usuarios.route('/<id>', methods=['DELETE'])
def DeleteUsuario(id):
    return 'DeleteUsuario'

@usuarios.route("/refresh", methods=["POST"])
def refresh():
    return refresh_token()

@usuarios.route('/logout', methods=['POST'])
def Logout():
    return logout()