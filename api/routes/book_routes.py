# book_routes.py
from flask import Blueprint, request, jsonify
from models.book import Book
from models.bookparticipant import BookParticipant
from models.participant import Participant
from models.role import Role
from models.base import db  # Import the SQLAlchemy db instance

book_bp = Blueprint('books', __name__)


@book_bp.route('/', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([book.json() for book in books])

@book_bp.route('/<int:id>', methods=['GET'])
def get_book_by_id(id):
    book = Book.find_by_id(id)
    return jsonify(book.json()) if book else ('Book not found', 404)


@book_bp.route('/', methods=['POST'])
def add_book():
    data = request.get_json()
    
    # Extract book information from the request
    title = data.get('title')
    isbn = data.get('isbn')
    description = data.get('description', None)
    edition_number = data.get('edition_number', None)
    publisher = data.get('publisher', None)
    publication_place = data.get('publication_place', None)
    publication_date = data.get('publication_date', None)
    number_of_pages = data.get('number_of_pages', None)

    # Create the Book instance but don't commit yet
    book = Book(title=title, isbn=isbn, description=description, edition_number=edition_number,
                publisher=publisher, publication_place=publication_place,
                publication_date=publication_date, number_of_pages=number_of_pages)

    # Initialize a list to collect errors about non-existing participants
    errors = []

    # Handle participants and roles, ensuring participants exist
    participants = data.get('participants', [])
    for participant_info in participants:
        participant_name = participant_info.get('name')
        role_description = participant_info.get('role')

        # Check if the participant exists
        participant = Participant.query.filter_by(name=participant_name).first()
        if not participant:
            errors.append(f"Participant '{participant_name}' not found.")
            continue

        # Check if the role exists, create if not
        role = Role.query.filter_by(description=role_description).first()
        if not role:
            role = Role(description=role_description)
            db.session.add(role)

        # Create the BookParticipant association without committing yet
        book_participant = BookParticipant(participant_id=participant.id, role_id=role.id)
        book.participants.append(book_participant)

    # If there were any errors, don't commit and return an error response
    if errors:
        db.session.rollback()  # Ensure no changes are made if there are errors
        return jsonify({'errors': errors}), 400

    # If all participants exist, commit the new book and its associations to the database
    book.save_to_db()

    return jsonify(book.json()), 201


@book_bp.route('/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.get_json()
    
    # Attempt to find the book
    book = Book.find_by_id(book_id)
    if not book:
        return jsonify({'message': 'Book not found'}), 404
    
    # Update basic book details
    for attribute in ['title', 'isbn', 'description', 'edition_number', 'publisher', 
                      'publication_place', 'publication_date', 'number_of_pages']:
        if attribute in data:
            setattr(book, attribute, data[attribute])
    
    # Initialize list to collect errors
    errors = []
    
    # Process participants and roles update
    for participant_info in data.get('participants', []):
        participant_name = participant_info.get('name')
        new_role_description = participant_info.get('new_role')
        
        # Attempt to find the participant by name
        participant = Participant.query.filter_by(name=participant_name).first()
        if not participant:
            errors.append(f"Participant '{participant_name}' not found.")
            continue
        
        # Attempt to find or create the role
        role = Role.query.filter_by(description=new_role_description).first()
        if not role:
            role = Role(description=new_role_description)
            db.session.add(role)
        
        # Attempt to find existing BookParticipant relation
        book_participant = BookParticipant.query.filter_by(book_id=book.id, participant_id=participant.id).first()
        if book_participant:
            book_participant.role_id = role.id
        else:
            # If the relation does not exist, create a new one
            new_book_participant = BookParticipant(book_id=book.id, participant_id=participant.id, role_id=role.id)
            db.session.add(new_book_participant)
    
    if errors:
        db.session.rollback()  # Rollback any changes if there are errors
        return jsonify({'errors': errors}), 400
    
    db.session.commit()
    return jsonify(book.json()), 200

@book_bp.route('/<int:book_id>', methods=['PATCH'])
def patch_book(book_id):
    data = request.get_json()
    
    # Attempt to find the book
    book = Book.find_by_id(book_id)
    if not book:
        return jsonify({'message': 'Book not found'}), 404
    
    # Update book details if provided
    for attribute in ['title', 'isbn', 'description', 'edition_number', 'publisher', 
                      'publication_place', 'publication_date', 'number_of_pages']:
        if attribute in data:
            setattr(book, attribute, data[attribute])

    # Initialize a list to collect errors
    errors = []

    # Optionally process participants and roles update if provided
    if 'participants' in data:
        for participant_info in data['participants']:
            participant_name = participant_info.get('name')
            new_role_description = participant_info.get('role', None)
            
            participant = Participant.query.filter_by(name=participant_name).first()
            if not participant:
                errors.append(f"Participant '{participant_name}' not found.")
                continue

            if new_role_description:
                role = Role.query.filter_by(description=new_role_description).first()
                if not role:
                    role = Role(description=new_role_description)
                    db.session.add(role)
                book_participant = BookParticipant.query.filter_by(book_id=book.id, participant_id=participant.id).first()
                if book_participant:
                    book_participant.role_id = role.id
                else:
                    errors.append(f"BookParticipant relation for '{participant_name}' not found.")
            else:
                # If no new role provided, no action needed regarding roles
                pass

    if errors:
        db.session.rollback()
        return jsonify({'errors': errors}), 400

    db.session.commit()
    return jsonify(book.json()), 200

@book_bp.route('/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.find_by_id(id)
    if book:
        book.delete_from_db()
        return 'Book deleted', 200
    return 'Book not found', 404
