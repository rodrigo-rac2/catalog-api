# book.py
from .base import db, BaseModel
from flask_restx import fields, Namespace

# Create a dedicated namespace for book operations
api = Namespace('books', description='Book operations')

# Define book model for database
class Book(BaseModel):
    __tablename__ = 'books'
    
    bookid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    editionnumber = db.Column(db.Integer)
    publisher = db.Column(db.String(255))
    publicationplace = db.Column(db.String(255))
    publicationdate = db.Column(db.Date)
    numberofpages = db.Column(db.Integer)
    isbn = db.Column(db.String(255), unique=True, nullable=False)
    participants = db.relationship('BookParticipant', back_populates='book', cascade='all, delete-orphan')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # Utilize the parent class constructor for setting attributes

# API models for input/output serialization
participant_info_model = api.model('ParticipantInfo', {
    'participantid': fields.Integer(description='Participant ID', attribute='participantid'),
    'name': fields.String(description='Participant name')
})

role_info_model = api.model('RoleInfo', {
    'roleid': fields.Integer(description='Role ID', attribute='roleid'),
    'description': fields.String(description='Role description')
})

book_participant_model = api.model('BookParticipant', {
    'participant': fields.Nested(participant_info_model),
    'role': fields.Nested(role_info_model)
})

book_model = api.model('Book', {
    'id': fields.Integer(description='The book unique identifier', attribute='bookid'),
    'title': fields.String(required=True, description='Book title'),
    'description': fields.String(description='Book description'),
    'editionnumber': fields.Integer(description='Edition number of the book'),
    'publisher': fields.String(description='Book publisher'),
    'publicationplace': fields.String(description='Place of publication'),
    'publicationdate': fields.String(description='Publication date'),
    'numberofpages': fields.Integer(description='Number of pages'),
    'isbn': fields.String(required=True, description='ISBN number'),
    'participants': fields.List(fields.Nested(book_participant_model), description='Participants involved in the book', required=False)
})
