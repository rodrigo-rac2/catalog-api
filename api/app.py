#app.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
api = Api(app, version='1.0', title='Book Catalog API', description='A simple book catalog API')

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:password@catalog-db:5432/catalog')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from models.base import db
db.init_app(app)

from routes.participant_routes import api as participants_ns
from routes.book_routes import api as books_ns
from routes.role_routes import api as roles_ns

api.add_namespace(participants_ns, path='/api/participants')
api.add_namespace(books_ns, path='/api/books')
api.add_namespace(roles_ns, path='/api/roles')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5100)
