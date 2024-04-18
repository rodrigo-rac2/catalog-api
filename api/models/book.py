# book.py
from .base import db, BaseModel
from flask_restx import fields, Namespace

api = Namespace('books', description='Book operations')

class Book(BaseModel):
    __tablename__ = 'books'

    bookid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    editionnumber = db.Column('editionnumber', db.Integer)
    publisher = db.Column(db.String(255))
    publicationplace = db.Column('publicationplace', db.String(255))
    publicationdate = db.Column('publicationdate', db.Date)
    numberofpages = db.Column('numberofpages', db.Integer)
    isbn = db.Column(db.String(255), unique=True, nullable=False)

    participants = db.relationship('BookParticipant', back_populates='book', cascade='all, delete-orphan')

    def __init__(self, title, isbn, description=None, edition_number=None, publisher=None,
                 publication_place=None, publication_date=None, number_of_pages=None):
        self.title = title
        self.isbn = isbn
        self.description = description
        self.editionnumber = edition_number
        self.publisher = publisher
        self.publication_place = publication_place
        self.publication_date = publication_date
        self.number_of_pages = number_of_pages

book_model = api.model('Book', {
    'id': fields.Integer(description='The book unique identifier', attribute='bookid'),
    'title': fields.String(required=True, description='Book title'),
    'description': fields.String(description='Book description'),
    'editionnumber': fields.Integer(description='Edition number of the book'),
    'publisher': fields.String(description='Book publisher'),
    'publicationplace': fields.String(description='Place of publication'),
    'publicationdate': fields.String(description='Publication date'),
    'numberofpages': fields.Integer(description='Number of pages'),
    'isbn': fields.String(required=True, description='ISBN number')
})
