# book_routes.py
from flask_restx import Namespace, Resource, fields
from models import db, Book, BookParticipant, Participant
from sqlalchemy.orm import joinedload

api = Namespace('books', description='Book operations')

book_model = api.model('Book', {
    'bookid': fields.Integer(readOnly=True, description='The book unique identifier'),
    'title': fields.String(required=True, description='The book title'),
    'description': fields.String(description='The book description'),
    'editionnumber': fields.Integer(description='Edition number of the book'),
    'publisher': fields.String(description='The book publisher'),
    'publicationplace': fields.String(description='Where the book was published'),
    'publicationdate': fields.String(description='When the book was published'),
    'numberofpages': fields.Integer(description='Number of pages in the book'),
    'isbn': fields.String(required=True, description='The ISBN of the book'),
    'participants': fields.List(fields.Nested(api.model('BookParticipant', {
        'book_id': fields.Integer(description='Book identifier'),
        'participant': fields.Nested(api.model('Participant', {
            'participantid': fields.Integer(description='Participant ID'),
            'name': fields.String(description='Participant name')
        })),
        'role_id': fields.Integer(description='Role identifier')
    })))
})

@api.route('/')
class BookList(Resource):
    @api.marshal_list_with(book_model)
    def get(self):
        """List all books"""
        books = Book.query.options(
            joinedload(Book.participants).joinedload(BookParticipant.participant)
        ).all()
        return books

    @api.expect(book_model, validate=True)
    @api.marshal_with(book_model, code=201)
    def post(self):
        """Create a new book"""
        data = api.payload
        book = Book(**data)
        db.session.add(book)
        db.session.commit()
        return book, 201

@api.route('/<int:id>')
@api.param('id', 'The book identifier')
@api.response(404, 'Book not found')
class BookResource(Resource):
    @api.marshal_with(book_model)
    def get(self, id):
        """Fetch a book given its identifier"""
        book = Book.query.get_or_404(id)
        return book

    @api.expect(book_model)
    @api.response(204, 'Book successfully updated.')
    def put(self, id):
        """Update a book given its identifier"""
        book = Book.query.get_or_404(id)
        data = api.payload
        for key, value in data.items():
            setattr(book, key, value)
        db.session.commit()
        return book, 204

    @api.response(204, 'Book successfully deleted.')
    def delete(self, id):
        """Delete a book given its identifier"""
        book = Book.query.get_or_404(id)
        db.session.delete(book)
        db.session.commit()
        return 'Book deleted', 204
