# participant.py
from .base import db, BaseModel
from .bookparticipant import BookParticipant

class Participant(BaseModel):
    __tablename__ = 'participants'

    id = db.Column('participantid', db.Integer, primary_key=True)
    name = db.Column('name', db.String(255), nullable=False)

    # Change the backref name to 'participant_books_association'
    books = db.relationship('BookParticipant', back_populates='participant', cascade='all, delete-orphan')

    def __init__(self, name):
        self.name = name

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'books': [book_participant.book.title for book_participant in self.books]
        }
