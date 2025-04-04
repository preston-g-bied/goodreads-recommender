# database/models.py

from sqlalchemy.orm import relationship
from datetime import datetime
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from backend.app import db

class User(db.Model):
    """User model"""
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    joined_date = db.Column(db.DateTime, default=datetime.now)
    profile_image = db.Column(db.String(255))

    # relationships
    ratings = relationship('Rating', back_populates='user')
    to_read = relationship('ToRead', back_populates='user')

class Book(db.Model):
    """Book model"""
    __tablename__ = 'books'

    book_id = db.Column(db.Integer, primary_key=True)
    goodreads_book_id = db.Column(db.Integer)
    best_book_id = db.Column(db.Integer)
    work_id = db.Column(db.Integer)
    books_count = db.Column(db.Integer)
    isbn = db.Column(db.String(20))
    isbn13 = db.Column(db.Float)
    authors = db.Column(db.String(255))
    original_publication_year = db.Column(db.Float)
    original_title = db.Column(db.String(255))
    title = db.Column(db.String(255), nullable=False)
    language_code = db.Column(db.String(10))
    average_rating = db.Column(db.Float)
    ratings_count = db.Column(db.Integer)
    work_ratings_count = db.Column(db.Integer)
    work_text_reviews_count = db.Column(db.Integer)
    ratings_1 = db.Column(db.Integer)
    ratings_2 = db.Column(db.Integer)
    ratings_3 = db.Column(db.Integer)
    ratings_4 = db.Column(db.Integer)
    ratings_5 = db.Column(db.Integer)
    image_url = db.Column(db.String(255))
    small_image_url = db.Column(db.String(255))

    # relationships
    ratings = relationship('Rating', back_populates='book')
    to_read = relationship('ToRead', back_populates='book')
    book_tags = relationship('BookTag', back_populates='book')

class Rating(db.Model):
    """Ratings model"""
    __tablename__ = 'ratings'

    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(2000))
    timestamp = db.Column(db.DateTime, default=datetime.now)

    # relationships
    user = relationship('User', back_populates='ratings')
    book = relationship('Book', back_populates='ratings')

class ToRead(db.Model):
    """To Read model"""
    __tablename__ = 'to_read'

    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), primary_key=True)
    added_date = db.Column(db.DateTime, default=datetime.now)

    # relationships
    user = relationship('User', back_populates='to_read')
    book = relationship('Book', back_populates='to_read')

class Tag(db.Model):
    """Tag model"""
    __tablename__ = 'tags'

    tag_id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(100), nullable=False, unique=True)

    # relationships
    book_tags = relationship('BookTag', back_populates='tag')

class BookTag(db.Model):
    """Book Tag model"""
    __tablename__ = 'book_tags'

    # using a composite primary key
    goodreads_book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.tag_id'), primary_key=True)
    count = db.Column(db.Integer, default=1)

    # relationships
    book = relationship('Book', back_populates='book_tags')
    tag = relationship('Tag', back_populates='book_tags')

class UserActivity(db.Model):
    """User Activity model for tracking user activities"""
    __tablename__ = 'user_activity'

    activity_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    activity_type = db.Column(db.String(50))  # e.g., 'rate', 'add_to_read', 'view', etc.
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'))
    timestamp = db.Column(db.DateTime, default=datetime.now)
    details = db.Column(db.String(255))   # additional activity details if needed

class Recommendation(db.Model):
    """Recommendation model for storing generated recommendations"""
    __tablename__ = 'recommendations'

    recommendation_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'))
    score = db.Column(db.Float)   # recommendation score/confidence
    source = db.Column(db.String(50)) # algorithm/source of the recommendation
    generated_at = db.Column(db.DateTime, default=datetime.now)