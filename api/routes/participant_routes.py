# participant_routes.py is a blueprint for the participant routes

from flask import Blueprint, request, jsonify
from models.participant import Participant

participant_bp = Blueprint('participants', __name__)

@participant_bp.route('/', methods=['GET'])
def get_participants():
    participants = Participant.query.all()
    return jsonify([participant.json() for participant in participants])
    
@participant_bp.route('/<int:id>', methods=['GET'])
def get_participant_by_id(id):
    participant = Participant.find_by_id(id)
    return jsonify(participant.json()) if participant else ('Participant not found', 404)

@participant_bp.route('/', methods=['POST'])
def add_participant():
    data = request.get_json()
    participant = Participant(**data)
    participant.save_to_db()
    return jsonify(participant.json()), 201

@participant_bp.route('/<int:id>', methods=['PUT'])
def update_participant(id):
    data = request.get_json()
    participant = Participant.find_by_id(id)
    if participant:
        participant.update(**data)
        return jsonify(participant.json())
    return 'Participant not found', 404

@participant_bp.route('/<int:id>', methods=['DELETE'])
def delete_participant(id):
    participant = Participant.find_by_id(id)
    if participant:
        participant.delete_from_db()
        return 'Participant deleted', 200
    return 'Participant not found', 404
