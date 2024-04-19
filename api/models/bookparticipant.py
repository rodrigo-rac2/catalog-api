# bookparticipant.py
from .base import db, BaseModel
from flask_restx import fields, Namespace

api = Namespace('book_participants', description='Operations related to book participants')

class BookParticipant(BaseModel):
    __tablename__ = 'bookparticipants'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # New primary key
    bookid = db.Column('bookid', db.Integer, db.ForeignKey('books.bookid'))
    participantid = db.Column('participantid', db.Integer, db.ForeignKey('participants.participantid'))
    roleid = db.Column('roleid', db.Integer, db.ForeignKey('roles.roleid'))

    # Relationship declared with string references to avoid circular imports
    book = db.relationship('Book', back_populates='participants')
    participant = db.relationship('Participant', back_populates='books')
    role = db.relationship('Role', back_populates='book_participants')

book_participant_model = api.model('BookParticipant', {
    'id': fields.Integer(description='Book participant identifier', attribute='id'),  # New field 'id
    'bookid': fields.Integer(required=True, description='Book identifier', attribute='bookid'),
    'participant': fields.Nested(api.model('Participant', {
        'participantid': fields.Integer(description='Participant ID', attribute='participantid'),
        'name': fields.String(description='Participant name')
    })),
    'roleid': fields.Integer(required=True, description='Role identifier', attribute='roleid')
})
