# bookparticipant.py
from .base import db, BaseModel
from flask_restx import fields, Namespace

api = Namespace('book_participants', description='Operations related to book participants')

class BookParticipant(BaseModel):
    __tablename__ = 'bookparticipants'

    book_id = db.Column('bookid', db.Integer, db.ForeignKey('books.bookid'), primary_key=True)
    participant_id = db.Column('participantid', db.Integer, db.ForeignKey('participants.participantid'), primary_key=True)
    role_id = db.Column('roleid', db.Integer, db.ForeignKey('roles.roleid'), primary_key=True)

    # Relationship declared with string references to avoid circular imports
    book = db.relationship('Book', back_populates='participants')
    participant = db.relationship('Participant', back_populates='books')
    role = db.relationship('Role', back_populates='book_participants')

book_participant_model = api.model('BookParticipant', {
    'book_id': fields.Integer(required=True, description='Book identifier', attribute='book_id'),
    'participant': fields.Nested(api.model('Participant', {
        'participantid': fields.Integer(description='Participant ID', attribute='participant_id'),
        'name': fields.String(description='Participant name')
    })),
    'role_id': fields.Integer(required=True, description='Role identifier', attribute='role_id')
})
