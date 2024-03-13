from flask import Blueprint
from invoices.services.invoices import addInvoice

invoices = Blueprint('invoices', __name__)

@invoices.route('/addInvoice', methods=['POST'])
def createRegisterInvoice():
    return addInvoice()

