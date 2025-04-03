# data-processing/etl/extract.py

"""
Extract module - Reads raw data from source files
"""

import pandas as pd
import logging
from pathlib import Path
import sys

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

def extract_ratings():
    """Extract ratings data from CSV file"""
    logger.info(f'Extracting ratings data from {config.RATINGS_FILE}')
    try:
        df = pd.read_csv(config.RATINGS_FILE)
        logger.info(f'Successfully extracted {len(df)} ratings records')
        return df
    except Exception as e:
        logger.error(f"Error extracting ratings data: {e}")
        raise

def extract_to_read():
    """Extract to-read data from CSV file"""
    logger.info(f'Extracting to-read data from {config.TO_READ_FILE}')
    try:
        df = pd.read_csv(config.TO_READ_FILE)
        logger.info(f'Successfully extracted {len(df)} to-read records')
        return df
    except Exception as e:
        logger.error(f"Error extracting to-read data: {e}")
        raise

def extract_books():
    """Extract books data from CSV file"""
    logger.info(f'Extracting books data from {config.BOOKS_FILE}')
    try:
        df = pd.read_csv(config.BOOKS_FILE)
        logger.info(f'Successfully extracted {len(df)} books records')
        return df
    except Exception as e:
        logger.error(f"Error extracting books data: {e}")
        raise

def extract_book_tags():
    """Extract book tags data from CSV file"""
    logger.info(f'Extracting book tags data from {config.BOOK_TAGS_FILE}')
    try:
        df = pd.read_csv(config.BOOK_TAGS_FILE)
        logger.info(f'Successfully extracted {len(df)} book tags records')
        return df
    except Exception as e:
        logger.error(f"Error extracting book tags data: {e}")
        raise

def extract_tags():
    """Extract tags data from CSV file"""
    logger.info(f'Extracting tags data from {config.TAGS_FILE}')
    try:
        df = pd.read_csv(config.TAGS_FILE)
        logger.info(f'Successfully extracted {len(df)} tags records')
        return df
    except Exception as e:
        logger.error(f"Error extracting tags data: {e}")
        raise

def extract_all():
    """Extract all data sources"""
    data = {}
    try:
        data['ratings'] = extract_ratings()
        data['to_read'] = extract_to_read()
        data['books'] = extract_books()
        data['book_tags'] = extract_book_tags()
        data['tags'] = extract_tags()
        return data
    except Exception as e:
        logger.error(f'Error in extract_all: {e}')
        raise

if __name__ == "__main__":
    # text extraction functionality
    extract_all()