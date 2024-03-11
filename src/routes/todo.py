from flask import Blueprint
from services.todo import create_invoice_service

todo = Blueprint('invoices', __name__)

@todo.route('/', methods=['GET'])
def getInvoices():
    return 'get all invoices'

@todo.route('/', methods=['POST'])
def CreateInvoices():
    return create_invoice_service()

@todo.route('/<id>', methods=['GET'])
def getById(id):
    return 'getById'

@todo.route('/<id>', methods=['PUT'])
def UpdateInvoice(id):
    return 'UpdateInvoice'

@todo.route('/<id>', methods=['DELETE'])
def DeleteInvoice(id):
    return 'DeleteInvoice'