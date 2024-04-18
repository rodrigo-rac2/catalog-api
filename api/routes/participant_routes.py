# participant_routes.py

from flask_restx import Namespace, Resource, fields
from models import db, Participant

api = Namespace('participants', description='Participant operations')

participant_model = api.model('Participant', {
    'participantid': fields.Integer(readOnly=True, description='The participant unique identifier', attribute='participantid'),
    'name': fields.String(required=True, description='The name of the participant')
})

@api.route('/')
class ParticipantList(Resource):
    @api.marshal_list_with(participant_model)
    def get(self):
        """List all participants"""
        participants = Participant.query.all()
        return participants

@api.route('/<int:participantid>')
@api.param('participantid', 'The participant identifier')
@api.response(404, 'Participant not found')
class ParticipantResource(Resource):
    @api.marshal_with(participant_model)
    def get(self, participantid):
        """Fetch a participant given their identifier"""
        participant = Participant.query.get_or_404(participantid)
        return participant

    @api.expect(participant_model)
    @api.response(204, 'Participant successfully updated.')
    def put(self, participantid):
        """Update a participant given their identifier"""
        participant = Participant.query.get_or_404(participantid)
        data = api.payload
        for key, value in data.items():
            setattr(participant, key, value)
        db.session.commit()
        return participant, 204

    @api.response(204, 'Participant successfully deleted.')
    def delete(self, participantid):
        """Delete a participant given their identifier"""
        participant = Participant.query.get_or_404(participantid)
        db.session.delete(participant)
        db.session.commit()
        return 'Participant deleted', 204
