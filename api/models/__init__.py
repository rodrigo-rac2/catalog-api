# models/__init__.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Initialize SQLAlchemy once and import it from here elsewhere

from .book import Book
from .participant import Participant
from .role import Role
from .bookparticipant import BookParticipant

__all__ = ['db', 'Book', 'Participant', 'Role', 'BookParticipant']
