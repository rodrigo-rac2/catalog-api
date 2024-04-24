# participant_routes.py

from flask import current_app
from flask_restx import Namespace, Resource, fields
from sqlalchemy.exc import IntegrityError
from models import db, Participant

api = Namespace('participants', description='Participant operations')

participant_model = api.model('Participant', {
    'participantid': fields.Integer(readOnly=True, description='The participant unique identifier', attribute='participantid'),
    'name': fields.String(required=True, description='The name of the participant')
})

participant_name = api.model('ParticipantName', {
    'name': fields.String(required=True, description='The name of the participant')
})

@api.route('/')
class ParticipantList(Resource):
    @api.marshal_list_with(participant_model)
    def get(self):
        """List all participants"""
        try:
            participants = Participant.query.all()
            return participants
        except Exception as e:
            current_app.logger.error(f"Error retrieving participants: {e}")
            return {"message": "Error retrieving participants"}, 500

    @api.expect(participant_name, validate=True)
    @api.marshal_with(participant_model, code=201)
    def post(self):
        """Create a new participant"""
        data = api.payload
        participant = Participant(name=data['name'])
        db.session.add(participant)
        try:
            db.session.commit()
            return participant, 201
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Failed to add participant: {e}")
            return {"message": "Failed to add participant"}, 500

@api.route('/<int:participantid>')
@api.param('participantid', 'The participant identifier')
@api.response(404, 'Participant not found')
class ParticipantResource(Resource):
    @api.marshal_with(participant_model)
    def get(self, participantid):
        """Fetch a participant given their identifier"""
        participant = Participant.query.get(participantid)
        if participant:
            return participant
        else:
            api.abort(404, f"Participant with ID {participantid} not found")

    @api.expect(participant_name)
    @api.response(204, 'Participant successfully updated.')
    @api.marshal_with(participant_model)  
    def put(self, participantid):
        """Update a participant given their identifier"""
        participant = Participant.query.get(participantid)
        if not participant:
            api.abort(404, f"Participant with ID {participantid} not found")
        data = api.payload
        for key, value in data.items():
            if hasattr(participant, key):
                setattr(participant, key, value)
        db.session.commit()
        return participant, 204

    @api.response(204, 'Participant successfully deleted.')
    def delete(self, participantid):
        """Delete a participant given their identifier"""
        participant = Participant.query.get(participantid)
        if not participant:
            api.abort(404, f"Participant with ID {participantid} not found")
        try: 
            db.session.delete(participant)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            current_app.logger.error(f"Cannot delete participant ({participantid}) as it is currently assigned to one or more books: {e}")
            return {'message': 'Cannot delete participant ({participantid}) as it is currently assigned to one or more books'}, 500
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Failed to delete participant ({participantid}): {e}")
            return {'message': 'Failed to delete participant ({participantid})'}, 500
        return {'message': 'Participant deleted'}, 204
