# data-processing/etl/load.py

"""
Load module - Saves transformed data to files and database
"""

import pandas as pd
import logging
import os
from pathlib import Path
import sys
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# add parent directory to path to import config
sys.path.append(str(Path(__file__).resolve().parent.parent))
import config

# set up logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format=config.LOG_FORMAT,
    handlers=[
        logging.FileHandler(config.LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# setup database connection
Base = declarative_base()

def save_to_csv(data_dict):
    """Save cleaned data to CSV files"""
    logger.info('Saving cleaned data to CSV files')

    # create the processed data directory if it doesn't exist
    os.makedirs(config.PROCESSED_DATA_DIR, exist_ok=True)

    # save each dataframe to its respective CSV file
    data_dict['ratings'].to_csv(config.CLEAN_RATINGS_FILE, index=False)
    logger.info(f'Saved clean ratings to {config.CLEAN_RATINGS_FILE}')

    data_dict['to_read'].to_csv(config.CLEAN_TO_READ_FILE, index=False)
    logger.info(f'Saved clean to-read to {config.TO_READ_FILE}')

    data_dict['books'].to_csv(config.CLEAN_BOOKS_FILE, index=False)
    logger.info(f'Saved clean books to {config.CLEAN_BOOKS_FILE}')

    data_dict['book_tags'].to_csv(config.CLEAN_BOOK_TAGS_FILE, index=False)
    logger.info(f'Saved clean book tags to {config.CLEAN_BOOK_TAGS_FILE}')

    data_dict['tags'].to_csv(config.CLEAN_TAGS_FILE, index=False)
    logger.info(f'Saved clean tags to {config.CLEAN_TAGS_FILE}')

    return True

def create_db_tables(engine):
    """Create database tables if they don't exist"""
    # define the SQLAlchemy models (matching ERD)

    # define Book model
    class Book(Base):
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
        title = Column(String(255))
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

    # define Rating model
    class Rating(Base):
        __tablename__ = 'ratings'

        user_id = Column(Integer, primary_key=True)
        book_id = Column(Integer, ForeignKey('books.book_id'), primary_key=True)
        rating = Column(Integer)

    # define ToRead model
    class ToRead(Base):
        __tablename__ = 'to_read'

        user_id = Column(Integer, primary_key=True)
        book_id = Column(Integer, ForeignKey('books.book_id'), primary_key=True)

    # define Tag model
    class Tag(Base):
        __tablename__ = 'tags'

        tag_id = Column(Integer, primary_key=True)
        tag_name = Column(String(100))

    # define BookTag model
    class BookTag(Base):
        __tablename__ = 'book_tags'

        goodreads_book_id = Column(Integer, primary_key=True)
        tag_id = Column(Integer, ForeignKey('tags.tag_id'), primary_key=True)
        count = Column(Integer)

    # create all tables
    Base.metadata.create_all(engine)
    logger.info('Database tables created')

def load_to_database(data_dict):
    """Load cleaned data to database"""
    logger.info('Loading data to database')

    try:
        # create database engine
        engine = create_engine(config.DATABASE_URI)

        # create tables if they don't exist
        create_db_tables(engine)

        # load data into database
        data_dict['books'].to_sql('books', engine, if_exists='replace', index=False)
        logger.info(f"Loaded {len(data_dict['books'])} books into database")

        data_dict['ratings'].to_sql('ratings', engine, if_exists='replace', index=False)
        logger.info(f"Loaded {len(data_dict['ratings'])} ratings into database")

        data_dict['to_read'].to_sql('to_read', engine, if_exists='replace', index=False)
        logger.info(f"Loaded {len(data_dict['to_read'])} to-read entries into database")

        data_dict['tags'].to_sql('tags', engine, if_exists='replace', index=False)
        logger.info(f"Loaded {len(data_dict['tags'])} tags into database")

        data_dict['book_tags'].to_sql('book_tags', engine, if_exists='replace', index=False)
        logger.info(f"Loaded {len(data_dict['book_tags'])} book tags into database")

        return True
    
    except Exception as e:
        logger.error(f'Error loading data to database: {e}')
        return False