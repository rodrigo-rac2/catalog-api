# book_routes.py
from flask import current_app
from flask_restx import Namespace, Resource, fields, reqparse
from sqlalchemy.exc import IntegrityError
from models import db, Book, BookParticipant, Participant, Role

api = Namespace('books', description='Book operations')

# Define participant and role information models

book_info_model = api.model('BookInfo', {
    'bookid': fields.Integer(description='Book ID', attribute='bookid'),
    'title': fields.String(description='Book title')
})

book_id_model = api.model('BookId', {
    'bookid': fields.Integer(description='Book ID', attribute='bookid')
})

participant_info_model = api.model('ParticipantInfo', {
    'participantid': fields.Integer(description='Participant ID', attribute='participantid'),
    'name': fields.String(description='Participant name')
})

participant_id_model = api.model('ParticipantId', {
    'participantid': fields.Integer(description='Participant ID', attribute='participantid')
})

role_info_model = api.model('RoleInfo', {
    'roleid': fields.Integer(description='Role ID', attribute='roleid'),
    'description': fields.String(description='Role description')
})

role_id_model = api.model('RoleId', {
    'roleid': fields.Integer(description='Role ID', attribute='roleid')
})

book_participant_role_model = api.model('BookParticipantRole', {
    'book': fields.Nested(book_info_model),
    'participant': fields.Nested(participant_info_model),
    'role': fields.Nested(role_info_model)
})

book_participant_model = api.model('BookParticipant', {
    'participant': fields.Nested(participant_info_model),
    'role': fields.Nested(role_info_model)
})

book_participant_id_model = api.model('BookParticipantId', {
    'participant': fields.Nested(participant_id_model),
    'role': fields.Nested(role_id_model)
})

# Define a model for POST requests specifically
book_post_model = api.model('BookPost', {
    'title': fields.String(required=True, description='Book title'),
    'description': fields.String(description='Book description'),
    'editionnumber': fields.Integer(description='Edition number of the book'),
    'publisher': fields.String(description='Book publisher'),
    'publicationplace': fields.String(description='Place of publication'),
    'publicationdate': fields.String(description='Publication date'),
    'numberofpages': fields.Integer(description='Number of pages'),
    'isbn': fields.String(required=True, description='ISBN number')
})

# Main book model incorporating nested models
book_model = api.model('Book', {
    'bookid': fields.Integer(readOnly=True, description='The book unique identifier'),
    'title': fields.String(required=True, description='Book title'),
    'description': fields.String(description='Book description'),
    'editionnumber': fields.Integer(description='Edition number of the book'),
    'publisher': fields.String(description='Book publisher'),
    'publicationplace': fields.String(description='Place of publication'),
    'publicationdate': fields.String(description='Publication date'),
    'numberofpages': fields.Integer(description='Number of pages'),
    'isbn': fields.String(required=True, description='ISBN number'),
    'participants': fields.List(fields.Nested(book_participant_model), description='Participants involved in the book', required=False)
})

# Argument parser for GET request filtering
parser = reqparse.RequestParser()
parser.add_argument('title', type=str, help='Filter by book title')
parser.add_argument('isbn', type=str, help='Filter by ISBN')
parser.add_argument('publisher', type=str, help='Filter by publisher')
parser.add_argument('editionnumber', type=int, help='Filter by edition number')
parser.add_argument('publicationplace', type=str,
                    help='Filter by publication place')
parser.add_argument('publicationdate', type=str,
                    help='Filter by publication date like year')
parser.add_argument('participant_name', type=str,
                    help='Filter by participant name')


@api.route('/')
class BookList(Resource):
    @api.expect(parser)
    @api.marshal_list_with(book_model)
    def get(self):
        """List all books or filter books based on query parameters."""
        args = parser.parse_args()  # Parse arguments from query

        # Start the query with joinedload options for efficient loading of relationships
        query = Book.query.options(
            db.joinedload(Book.participants).joinedload(
                BookParticipant.participant),
            db.joinedload(Book.participants).joinedload(BookParticipant.role)
        )

        # Apply filters based on arguments provided
        if args['title']:
            query = query.filter(Book.title.ilike(f'%{args["title"]}%'))
        if args['isbn']:
            query = query.filter(Book.isbn == args['isbn'])
        if args['publisher']:
            query = query.filter(
                Book.publisher.ilike(f'%{args["publisher"]}%'))
        if args['editionnumber'] is not None:
            query = query.filter(Book.editionnumber == args['editionnumber'])
        if args['publicationplace']:
            query = query.filter(Book.publicationplace.ilike(
                f'%{args["publicationplace"]}%'))
        if args['publicationdate']:
            query = query.filter(Book.publicationdate.like(
                f'%{args["publicationdate"]}%'))
        if args['participant_name']:
            query = query.join(BookParticipant).join(Participant).filter(
                Participant.name.ilike(f'%{args["participant_name"]}%'))

        # Execute the query and return results
        books = query.all()
        return books

    @api.expect(book_post_model, validate=True)
    @api.marshal_with(book_model, code=201)
    def post(self):
        """Create a new book"""
        data = api.payload.copy()
        participants_data = data.pop('participants', [])

        try:
            # Convert editionnumber and numberofpages to integers if they are not None
            if 'editionnumber' in data:
                data['editionnumber'] = int(data['editionnumber'])
            if 'numberofpages' in data:
                data['numberofpages'] = int(data['numberofpages'])
            
            # Create the book without the participants data
            book = Book(**data)
            db.session.add(book)
            db.session.commit()
            
            current_app.logger.info(f"New book added with ID {book.bookid}")

            return book, 201
        except IntegrityError as ie:
            db.session.rollback()
            current_app.logger.warning(f"Attempt to add duplicate book with ISBN {data.get('isbn')}")
            if 'isbn' in str(ie):
                return {"message": "A book with this ISBN already exists."}, 409
            return {"message": "Failed to add book due to a database error."}, 400
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Failed to add book: {e}")
            return {"message": f"Failed to add book due to an unexpected error: {str(e)}"}, 500


@api.route('/<int:bookid>')
@api.param('bookid', 'The book identifier')
@api.response(404, 'Book not found')
class BookResource(Resource):
    @api.marshal_with(book_model)
    def get(self, bookid):
        """Fetch a book given its identifier"""
        book = Book.query.options(
            db.joinedload(Book.participants).joinedload(
                BookParticipant.participant),
            db.joinedload(Book.participants).joinedload(BookParticipant.role)
        ).get_or_404(bookid)
        return book

    @api.expect(book_post_model)
    @api.response(204, 'Book successfully updated.')
    @api.marshal_with(book_model)
    def put(self, bookid):
        """Update a book given its identifier"""
        book = Book.query.get_or_404(bookid)
        data = api.payload
        try:
            for key, value in data.items():
                if key in ['editionnumber', 'numberofpages'] and value is not None:
                    value = int(value)  # Convert to integer if necessary
                setattr(book, key, value)
            db.session.commit()
            current_app.logger.info(f"Book updated with ID {book.bookid}")
            return book, 204
        except ValueError as ve:
            # Handle ValueError if integer conversion fails
            db.session.rollback()
            current_app.logger.error(f"Failed to update book due to type mismatch: {ve}")
            return {"message": "Invalid input, integer required: " + str(ve)}, 400
        except IntegrityError as ie:
            # Handle any integrity errors from the database
            db.session.rollback()
            current_app.logger.error(f"Attempt to update book to an existing ISBN: {data.get('isbn')}")
            return {"message": "Integrity error occurred: " + str(ie)}, 400
        except Exception as e:
            # Handle other exceptions
            db.session.rollback()
            current_app.logger.error(f"Failed to update book: {e}")
            return {"message": "Failed to update book: " + str(e)}, 500

    @api.response(204, 'Book successfully deleted.')
    def delete(self, bookid):
        """Delete a book given its identifier"""
        book = Book.query.get_or_404(bookid)
        try:
            db.session.delete(book)
            db.session.commit()
            return 'Book deleted', 204
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Failed to delete book: {e}")
            return {"message": "Failed to delete book"}, 500


@api.route('/<int:bookid>/participants')
@api.param('bookid', 'The book identifier')
class BookParticipantList(Resource):
    @api.marshal_list_with(book_participant_role_model)
    def get(self, bookid):
        """Get all participants associated with a specific book."""
        book = Book.query.get(bookid)
        if not book:
            api.abort(404, "Book not found")

        # Load participants with their corresponding roles
        participants = BookParticipant.query.options(
            db.joinedload(BookParticipant.participant),
            db.joinedload(BookParticipant.role)
        ).filter(BookParticipant.bookid == bookid).all()

        if not participants:
            return {"message": "No participants found for this book"}, 404

        return participants, 200

    @api.expect(book_participant_id_model, validate=True)
    @api.response(201, 'Participant added to book.')
    @api.response(400, 'Bad request.')
    @api.response(404, 'Book or participant not found.')
    def post(self, bookid):
        """Add a participant to a book"""
        data = api.payload

        # Validate that the book exists
        book = Book.query.get(bookid)
        if not book:
            return {"message": "Book not found"}, 404

        # Extract participant and role IDs from the nested structure
        participant_id = data.get('participant', {}).get('participantid')
        role_id = data.get('role', {}).get('roleid')

        try:
            # Fetch participant and role by IDs
            participant = Participant.query.get(
                participant_id) if participant_id else None
            role = Role.query.get(role_id) if role_id else None

            if not participant or not role:
                return {"message": "Invalid participant ID or role ID"}, 400

            # Create and add the new BookParticipant entry
            book_participant = BookParticipant(
                bookid=bookid, participantid=participant.participantid, roleid=role.roleid)
            db.session.add(book_participant)
            db.session.commit()
            return {"message": "Participant added successfully"}, 201

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Failed to add participant to book: {e}")
            return {"message": "Failed to add participant to book"}, 500
        
@api.route('/<int:bookid>/roles/<int:roleid>/participants')
@api.param('bookid', 'The book identifier')
@api.param('roleid', 'The role identifier')
class BookRoleList(Resource):
    @api.marshal_list_with(book_participant_role_model)
    def get(self, bookid, roleid):
        """Get all participants of role associated with a specific book."""
        book = Book.query.get(bookid)
        if not book:
            api.abort(404, "Book not found")

        # Load participants with their corresponding roles
        participants = BookParticipant.query.options(
            db.joinedload(BookParticipant.participant),
            db.joinedload(BookParticipant.role)
        ).filter(BookParticipant.bookid == bookid, BookParticipant.roleid == roleid).all()

        if not participants:
            return {"message": "No participants found for this book"}, 404

        return participants, 200


@api.route('/<int:bookid>/participants/<int:participantid>/role/<int:roleid>')
@api.param('bookid', 'The book identifier')
@api.param('participantid', 'The participant identifier')
@api.param('roleid', 'The role identifier to assign to the participant')
class BookParticipantUpdateResource(Resource):
    @api.response(204, 'Participant role updated successfully.')
    @api.response(400, 'Bad request.')
    @api.response(404, 'Book, participant or role not found.')
    def put(self, bookid, participantid, roleid):
        """Update a specific participant's role in a book."""
        # Validate book exists
        if not Book.query.get(bookid):
            return {"message": "Book not found"}, 404

        # Fetch the book participant entry
        book_participant = BookParticipant.query.filter_by(
            bookid=bookid, participantid=participantid).first()
        if not book_participant:
            return {"message": "Participant not found in this book"}, 404

        # Validate the new role exists
        role = Role.query.get(roleid)
        if not role:
            return {"message": "Role not found"}, 404

        # Update the role ID for the participant
        book_participant.roleid = roleid
        db.session.commit()
        return {"message": "Participant role updated successfully"}, 204


@api.route('/<int:bookid>/participants/<int:participantid>')
@api.param('bookid', 'The book identifier')
@api.param('participantid', 'The participant identifier')
class BookParticipantDeleteResource(Resource):
    @api.response(204, 'Participant deleted successfully.')
    @api.response(404, 'Participant not found in this book.')
    def delete(self, bookid, participantid):
        """Delete a participant from a book"""
        book_participant = BookParticipant.query.filter_by(
            bookid=bookid, participantid=participantid).first()
        if not book_participant:
            return {"message": "Participant not found in this book"}, 404

        try:
            db.session.delete(book_participant)
            db.session.commit()
            return '', 204

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Failed to delete participant: {e}")
            return {"message": "Failed to delete participant"}, 500
