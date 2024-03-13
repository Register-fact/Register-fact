from flask import Flask, request, jsonify
from auth.routes.auth import usuarios
from dotenv import load_dotenv
from config.mongodb import mongo
import os
from flask_jwt_extended import JWTManager

load_dotenv()

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
mongo.init_app(app)


jwt = JWTManager(app)



app.register_blueprint(usuarios, url_prefix='/')

if __name__ == '__main__':
    app.run(debug=True)

