# role.py
from .base import db, BaseModel

class Role(BaseModel):
    __tablename__ = 'roles'

    id = db.Column('roleid', db.Integer, primary_key=True)
    description = db.Column('description', db.String(255), unique=True, nullable=False)

    participants = db.relationship('BookParticipant', back_populates='role', cascade='all, delete-orphan')

    def __init__(self, description):
        self.description = description

    def json(self):
        return {
            'id': self.id,
            'description': self.description,
            'participants': [book_participant.participant.name for book_participant in self.participants]
        }
