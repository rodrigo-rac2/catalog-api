# role_routes.py
from flask import current_app
from flask_restx import Namespace, Resource, fields, reqparse
from sqlalchemy.sql import select
from sqlalchemy.exc import IntegrityError
from models import db, Role, BookParticipant

api = Namespace('roles', description='Role operations')

role_description_model = api.model('RoleDescription', {
    'description': fields.String(required=True, description='Role description')
})

role_model = api.model('Role', {
    'roleid': fields.Integer(readOnly=True, description='Role ID', attribute='roleid'),
    'description': fields.String(required=True, description='Role description')
})

# Argument parser for GET request filtering
parser = reqparse.RequestParser()
parser.add_argument('description', type=str,
                    help='Filter by role description')

@api.route('/')
class RoleList(Resource):
    @api.expect(parser)
    @api.marshal_list_with(role_model)
    def get(self):
        """List all roles"""
        args = parser.parse_args()  # Parse arguments from query
        query = Role.query
        try:
            # Apply filters based on arguments provided
            if args['description']:
                query = query.filter(Role.description.ilike(f'%{args["description"]}%'))
            roles = query.all()
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
    
        # Prepare a subquery for exist check
        subquery = db.session.query(BookParticipant.roleid).filter(BookParticipant.roleid == id).exists()
        # Check if the role is assigned to any participants
        if db.session.query(subquery).scalar():
            api.abort(400, f"Role with ID {id} is currently assigned to participants and cannot be deleted.")
    
        try:
            db.session.delete(role)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            current_app.logger.error(f"Cannot delete role ({id}) as it is currently assigned to one or more participants: {e}")
            api.abort(400, f"Cannot delete role ({id}) as it is currently assigned to one or more participants.")
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Failed to delete role ({id}): {e}")
            api.abort(500, f'Failed to delete role ({id})')
    
        return {'message': 'Role deleted'}, 204
