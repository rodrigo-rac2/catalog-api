# bookparticipant.py
from .base import db, BaseModel

class BookParticipant(BaseModel):
    __tablename__ = 'bookparticipants'

    book_id = db.Column('bookid', db.Integer, db.ForeignKey('books.bookid'), primary_key=True)
    participant_id = db.Column('participantid', db.Integer, db.ForeignKey('participants.participantid'), primary_key=True)
    role_id = db.Column('roleid', db.Integer, db.ForeignKey('roles.roleid'), primary_key=True)

    # Define relationships with updated backref names
    book = db.relationship('Book', back_populates='participants')
    participant = db.relationship('Participant', back_populates='books')
    role = db.relationship('Role', back_populates='participants')

    def __init__(self, book_id, participant_id, role_id):
        self.book_id = book_id
        self.participant_id = participant_id
        self.role_id = role_id
