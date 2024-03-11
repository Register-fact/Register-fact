from flask import Flask
from auth.routes.auth import usuarios
from dotenv import load_dotenv
from config.mongodb import mongo
import os

load_dotenv()

app = Flask(__name__)

app.config['MONGO_URI'] = os.getenv('MONGO_URI')
mongo.init_app(app)

@app.route('/')
def index():
    return 'hola'

app.register_blueprint(usuarios, url_prefix='/login')

if __name__ == '__main__':
    app.run(debug=True)

