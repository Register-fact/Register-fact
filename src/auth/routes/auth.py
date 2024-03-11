from flask import Blueprint
from auth.services.usuarios import create_usuario_service

usuarios = Blueprint('usuarios', __name__)

@usuarios.route('/', methods=['GET'])
def getUsuario():
    return 'get all usuario'

@usuarios.route('/', methods=['POST'])
def CreateUsuario():
    return create_usuario_service()

@usuarios.route('/<id>', methods=['GET'])
def getById(id):
    return 'getById'

@usuarios.route('/<id>', methods=['PUT'])
def UpdateUsuario(id):
    return 'UpdateUsuario'

@usuarios.route('/<id>', methods=['DELETE'])
def DeleteUsuario(id):
    return 'DeleteUsuario'