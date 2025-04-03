# database/models.py

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class User(Base):
    """User model"""
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    joined_date = Column(DateTime, default=datetime.now())
    profile_image = Column(String(255))

    # relationships
    ratings = relationship('Rating', back_populates='user')
    to_read = relationship('ToRead', back_populates='user')

class Book(Base):
    """Book model"""
    __tablename__ = 'books'

    book_id = Column(Integer, primary_key=True)
    goodreads_book_id = Column(Integer)
    best_book_id = Column(Integer)
    work_id = Column(Integer)
    books_count = Column(Integer)
    isbn = Column(String(20))
    isbn13 = Column(Float)
    authors = Column(String(255))
    original_publication_year = Column(Float)
    original_title = Column(String(255))
    title = Column(String(255), nullable=False)
    language_code = Column(String(10))
    average_rating = Column(Float)
    ratings_count = Column(Integer)
    work_ratings_count = Column(Integer)
    work_text_reviews_count = Column(Integer)
    ratings_1 = Column(Integer)
    ratings_2 = Column(Integer)
    ratings_3 = Column(Integer)
    ratings_4 = Column(Integer)
    ratings_5 = Column(Integer)
    image_url = Column(String(255))
    small_image_url = Column(String(255))

    # relationships
    ratings = relationship('Rating', back_populates='book')
    to_read = relationship('ToRead', back_populates='book')
    book_tags = relationship('BookTag', back_populates='book')

class Ratings(Base):
    """Ratings model"""
    __tablename__ = 'ratings'

    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    book_id = Column(Integer, ForeignKey('books.book_id'), primary_key=True)
    rating = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.now())

    # relationships
    user = relationship('User', back_populates='ratings')
    book = relationship('Book', back_populates='ratings')

class ToRead(Base):
    """To Read model"""
    __tablename__ = 'to_read'

    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    book_id = Column(Integer, ForeignKey('books.book_id'), primary_key=True)
    added_date = Column(DateTime, default=datetime.now())

    # relationships
    user = relationship('User', back_populates='to_read')
    book = relationship('Book', back_populates='to_read')

class Tag(Base):
    """Tag model"""
    __tablename__ = 'tags'

    tag_id = Column(Integer, primary_key=True)
    tag_name = Column(String(100), nullable=False, unique=True)

    # relationships
    book_tags = relationship('BookTag', back_populates='tag')

class BookTag(Base):
    """Book Tag model"""
    __tablename__ = 'book_tags'

    # using a composite primary key
    goodreads_book_id = Column(Integer, ForeignKey('books.book_id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tags.tag_id'), primary_key=True)
    count = Column(Integer, default=1)

    # relationships
    book = relationship('Book', back_populates='book_tags')
    tag = relationship('Tag', back_populates='book_tags')

class UserActivity(Base):
    """User Activity model for tracking user activities"""
    __tablename__ = 'user_activity'

    activity_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    activity_type = Column(String(50))  # e.g., 'rate', 'add_to_read', 'view', etc.
    book_id = Column(Integer, ForeignKey('books.book_id'))
    timestamp = Column(DateTime, default=datetime.now())
    details = Column(String(255))   # additional activity details if needed

class Recommendation(Base):
    """Recommendation model for storing generated recommendations"""
    __tablename__ = 'recommendations'

    recommendation_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    book_id = Column(Integer, ForeignKey('books.book_id'))
    score = Column(Float)   # recommendation score/confidence
    source = Column(String(50)) # algorithm/source of the recommendation
    generated_at = Column(DateTime, default=datetime.now())

def create_tables(engine_uri):
    """Create all tables in the database"""
    engine = create_engine(engine_uri)
    Base.metadata.create_all(engine)
    return engine