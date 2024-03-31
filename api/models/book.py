# book.py
from .base import db, BaseModel
from .bookparticipant import BookParticipant

class Book(BaseModel):
    __tablename__ = 'books'

    id = db.Column('bookid', db.Integer, primary_key=True)
    title = db.Column('title', db.String(255), nullable=False)
    description = db.Column('description', db.Text)
    edition_number = db.Column('editionnumber', db.Integer)
    publisher = db.Column('publisher', db.String(255))
    publication_place = db.Column('publicationplace', db.String(255))
    publication_date = db.Column('publicationdate', db.Date)
    number_of_pages = db.Column('numberofpages', db.Integer)
    isbn = db.Column('isbn', db.String(255), unique=True, nullable=False)
    
    # Update the backref name to 'book_participants_association'
    participants = db.relationship('BookParticipant', back_populates='book', cascade='all, delete-orphan')

    def __init__(self, title, isbn, description=None, edition_number=None, publisher=None,
                 publication_place=None, publication_date=None, number_of_pages=None):
        self.title = title
        self.isbn = isbn
        self.description = description
        self.edition_number = edition_number
        self.publisher = publisher
        self.publication_place = publication_place
        self.publication_date = publication_date
        self.number_of_pages = number_of_pages

    def json(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'edition_number': self.edition_number,
            'publisher': self.publisher,
            'publication_place': self.publication_place,
            'publication_date': self.publication_date.strftime('%Y-%m-%d') if self.publication_date else None,
            'number_of_pages': self.number_of_pages,
            'isbn': self.isbn,
            'participants': [book_participant.participant.name for book_participant in self.participants]
        }
