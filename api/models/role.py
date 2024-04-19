#role.py

from .base import db, BaseModel
from flask_restx import fields, Namespace

api = Namespace('roles', description='Role operations')

class Role(BaseModel):
    __tablename__ = 'roles'

    roleid = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), unique=True, nullable=False)

    # Ensure this matches the relationship defined in BookParticipant
    book_participants = db.relationship('BookParticipant', back_populates='role')

    role_model = api.model('Role', {
        'id': fields.Integer(description='Role ID', attribute='roleid'),
        'description': fields.String(required=True, description='Role description')
    })
