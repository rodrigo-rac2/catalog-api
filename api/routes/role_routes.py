# role_routes.py

from flask_restx import Namespace, Resource, fields
from models import Role, db  # Importing from centralized location

api = Namespace('roles', description='Role operations')

role_model = api.model('Role', {
    'roleid': fields.Integer(description='Role ID', attribute='roleid'),
    'description': fields.String(required=True, description='Role description')
})

@api.route('/')
class RoleList(Resource):
    @api.marshal_list_with(role_model)
    def get(self):
        """List all roles"""
        roles = Role.query.all()
        return roles

    @api.expect(role_model, validate=True)
    @api.marshal_with(role_model, code=201)
    def post(self):
        """Create a new role"""
        data = api.payload
        role = Role(description=data['description'])
        db.session.add(role)
        db.session.commit()
        return role, 201

@api.route('/<int:id>')
@api.param('id', 'The role identifier')
@api.response(404, 'Role not found')
class RoleResource(Resource):
    @api.marshal_with(role_model)
    def get(self, id):
        """Fetch a role given their identifier"""
        role = Role.query.get_or_404(id)
        return role

    @api.expect(role_model)
    @api.response(204, 'Role successfully updated.')
    def put(self, id):
        """Update a role given their identifier"""
        role = Role.query.get_or_404(id)
        data = api.payload
        if 'description' in data:
            role.description = data['description']
        db.session.commit()
        return role, 204

    @api.response(204, 'Role successfully deleted.')
    def delete(self, id):
        """Delete a role given their identifier"""
        role = Role.query.get_or_404(id)
        db.session.delete(role)
        db.session.commit()
        return 'Role deleted', 204
