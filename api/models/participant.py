# participant.py
from .base import db, BaseModel
from flask_restx import fields, Namespace

api = Namespace('participants', description='Participant operations')

class Participant(BaseModel):
    __tablename__ = 'participants'

    participantid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    # Use string for relationship to avoid circular import
    books = db.relationship('BookParticipant', back_populates='participant')

participant_model = api.model('Participant', {
    'participantid': fields.Integer(description='Participant ID', attribute='participant_id'),
    'name': fields.String(required=True, description='Participant name')
})