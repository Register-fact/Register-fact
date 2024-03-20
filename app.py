import os
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from datetime import timedelta
from config.mongodb import mongo
from auth.routes.auth import usuarios
from invoices.routes.InvoiceRoutes import invoices
from flask_cors import CORS


load_dotenv()

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
CORS(app, resources={r"/*": {"origins": "http://localhost:8081"}})
mongo.init_app(app)

""" def init_db(app):
    db = mongo.init_app(app)
    return db

init_db(app) """

jwt = JWTManager(app)


app.register_blueprint(usuarios, url_prefix='/')
app.register_blueprint(invoices, url_prefix='/usuario')

if __name__ == '__main__':
    app.run(debug=True)

