# participant_routes.py

from flask import current_app
from flask_restx import Namespace, Resource, fields, reqparse
from sqlalchemy import exists
from sqlalchemy.exc import IntegrityError
from models import db, Participant, BookParticipant

api = Namespace('participants', description='Participant operations')

participant_model = api.model('Participant', {
    'participantid': fields.Integer(readOnly=True, description='The participant unique identifier', attribute='participantid'),
    'name': fields.String(required=True, description='The name of the participant')
})

participant_name = api.model('ParticipantName', {
    'name': fields.String(required=True, description='The name of the participant')
})

# Argument parser for GET request filtering
parser = reqparse.RequestParser()
parser.add_argument('name', type=str,
                    help='Filter by participant name')

@api.route('/')
class ParticipantList(Resource):
    @api.expect(parser)
    @api.marshal_list_with(participant_model)
    def get(self):
        """List all participants"""
        args = parser.parse_args()  # Parse arguments from query
        query = Participant.query
        try:
            # Apply filters based on arguments provided
            if args['name']:
                query = query.filter(Participant.name.ilike(f'%{args["name"]}%'))
            participants = query.all()
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
        # Prepare a subquery for exist check
        subquery = db.session.query(BookParticipant.participantid).filter(BookParticipant.participantid == participantid).exists()
        # Check if the participant is assigned to any books
        if db.session.query(subquery).scalar():
            api.abort(400, f"Participant with ID {participantid} is currently assigned to a book and cannot be deleted.")

        try: 
            db.session.delete(participant)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            current_app.logger.error(f"Cannot delete participant ({participantid}) as it is currently assigned to one or more books: {e}")
            api.abort(400, f"Cannot delete participant ({participantid}) as it is currently assigned to one or more books.")  # Use api.abort to send the correct status and message
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Failed to delete participant ({participantid}): {e}")
            api.abort(500, f"Failed to delete participant ({participantid}).")  # Use api.abort to send the correct status and message
        return {'message': 'Participant deleted'}, 204
