# role_routes.py is a file that contains the routes for the Role model

from flask import Blueprint, request, jsonify
from models.role import Role

role_bp = Blueprint('roles', __name__)

@role_bp.route('/', methods=['GET'])
def get_roles():
    roles = Role.query.all()
    return jsonify([role.json() for role in roles])

@role_bp.route('/<int:id>', methods=['GET'])
def get_role_by_id(id):
    role = Role.find_by_id(id)
    return jsonify(role.json()) if role else ('Role not found', 404)

@role_bp.route('/', methods=['POST'])
def add_role():
    data = request.get_json()
    role = Role(**data)
    role.save_to_db()
    return jsonify(role.json()), 201

@role_bp.route('/<int:id>', methods=['PUT'])
def update_role(id):
    data = request.get_json()
    role = Role.find_by_id(id)
    if role:
        role.update(**data)
        return jsonify(role.json())
    return 'Role not found', 404

@role_bp.route('/<int:id>', methods=['DELETE'])
def delete_role(id):
    role = Role.find_by_id(id)
    if role:
        role.delete_from_db()
        return 'Role deleted', 200
    return 'Role not found', 404
