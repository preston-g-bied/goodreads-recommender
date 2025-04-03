# data-processing/config.py

"""
Configuration settings for ETL pipeline
"""

import os
from pathlib import Path

# base directory is repository root
BASE_DIR = Path(__file__).resolve().parent.parent

# data directories
RAW_DATA_DIR = os.path.join(BASE_DIR, 'data', 'raw')
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, 'data', 'processed')

# input files
RATINGS_FILE = os.path.join(RAW_DATA_DIR, 'ratings.csv')
TO_READ_FILE = os.path.join(RAW_DATA_DIR, 'to_read.csv')
BOOKS_FILE = os.path.join(RAW_DATA_DIR, 'books.csv')
BOOK_TAGS_FILE = os.path.join(RAW_DATA_DIR, 'book_tags.csv')
TAGS_FILE = os.path.join(RAW_DATA_DIR, 'tags.csv')

# output files
CLEAN_RATINGS_FILE = os.path.join(PROCESSED_DATA_DIR, 'ratings_clean.csv')
CLEAN_TO_READ_FILE = os.path.join(PROCESSED_DATA_DIR, 'to_read_clean.csv')
CLEAN_BOOKS_FILE = os.path.join(PROCESSED_DATA_DIR, 'books_clean.csv')
CLEAN_BOOK_TAGS_FILE = os.path.join(PROCESSED_DATA_DIR, 'book_tags_clean.csv')
CLEAN_TAGS_FILE = os.path.join(PROCESSED_DATA_DIR, 'tags_clean.csv')

# database connection
# update with actual database connection details
DATABASE_URI = 'sqlite:///database/goodbooks.db'    # for development
# for productions, consider using env variables:
# DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///database/goodbooks.db')

# logging configuration
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FILE = os.path.join(BASE_DIR, 'logs', 'etl.log')

# ensure directories exist
os.makedirs(os.path.join(BASE_DIR, 'logs'), exist_ok=True)
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)