# role_routes.py
from flask import current_app
from flask_restx import Namespace, Resource, fields
from models import db, Role

api = Namespace('roles', description='Role operations')

role_description_model = api.model('RoleDescription', {
    'description': fields.String(required=True, description='Role description')
})

role_model = api.model('Role', {
    'roleid': fields.Integer(readOnly=True, description='Role ID', attribute='roleid'),
    'description': fields.String(required=True, description='Role description')
})

@api.route('/')
class RoleList(Resource):
    @api.marshal_list_with(role_model)
    def get(self):
        """List all roles"""
        try:
            roles = Role.query.all()
            return roles
        except Exception as e:
            current_app.logger.error(f"Error retrieving roles: {e}")
            return {"message": "Error retrieving roles"}, 500

    @api.expect(role_description_model, validate=True)
    @api.marshal_with(role_model, code=201)
    def post(self):
        """Create a new role"""
        data = api.payload
        role = Role(description=data['description'])
        db.session.add(role)
        try:
            db.session.commit()
            return role, 201
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Failed to add role: {e}")
            return {"message": "Failed to add role"}, 500

@api.route('/<int:id>')
@api.param('id', 'The role identifier')
@api.response(404, 'Role not found')
class RoleResource(Resource):
    @api.marshal_with(role_model)
    def get(self, id):
        """Fetch a role given its identifier"""
        role = Role.query.get(id)
        if role:
            return role
        else:
            api.abort(404, f"Role with ID {id} not found")

    @api.expect(role_description_model)
    @api.response(204, 'Role successfully updated.')
    @api.marshal_with(role_model)  
    def put(self, id):
        """Update a role given its identifier"""
        role = Role.query.get(id)
        if not role:
            api.abort(404, f"Role with ID {id} not found")
        data = api.payload
        if 'description' in data:
            role.description = data['description']
        db.session.commit()
        return role, 204

    @api.response(204, 'Role successfully deleted.')
    def delete(self, id):
        """Delete a role given its identifier"""
        role = Role.query.get(id)
        if not role:
            api.abort(404, f"Role with ID {id} not found")
        db.session.delete(role)
        db.session.commit()
        return {'message': 'Role deleted'}, 204
