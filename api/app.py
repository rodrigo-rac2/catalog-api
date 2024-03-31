#app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:password@catalog-db:5432/catalog')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with app
from models.base import db
db.init_app(app)

# Import routes (ensure routes are imported after app initialization)
from routes.participant_routes import participant_bp
from routes.book_routes import book_bp
from routes.role_routes import role_bp

# Register Blueprints
app.register_blueprint(participant_bp, url_prefix='/api/participants')
app.register_blueprint(book_bp, url_prefix='/api/books')
app.register_blueprint(role_bp, url_prefix='/api/roles')

if __name__ == '__main__':
    app.run(debug=True if os.getenv('FLASK_ENV') == 'development' else False, host='0.0.0.0', port=5100)
