from flask import Blueprint
from invoices.services.invoices import addInvoice, get_all_invoices, get_invoice_by_id, delete_invoice, update_invoice_by_id

invoices = Blueprint('invoices', __name__)

@invoices.route('/addInvoice', methods=['POST'])
def createRegisterInvoice():
    return addInvoice()

@invoices.route('/getInvoices', methods=['GET'])
def Get_all_invoices():
    return get_all_invoices()

@invoices.route('/getInvoices/<string:invoice_id>', methods=['GET'])
def Get_invoice_by_id(invoice_id):
    return get_invoice_by_id(invoice_id)

@invoices.route('/deleteInvoice/<string:invoice_id>', methods=['DELETE'])
def Delete_invoice(invoice_id):
    return delete_invoice(invoice_id)

@invoices.route('/invoices/<string:invoice_id>', methods=['PUT'])
def update_invoice(invoice_id):
    return update_invoice_by_id(invoice_id)