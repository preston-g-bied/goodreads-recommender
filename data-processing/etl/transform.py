# data-processing/etl/transform.py

"""
Transform module - Cleans and processes extracted data
"""

import pandas as pd
import numpy as np
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

def clean_ratings(df):
    """Clean ratings data"""
    logger.info('Cleaning ratings data')

    df_clean = df.copy()

    # check for and remove duplicates
    duplicates = df_clean.duplicated(['user_id', 'book_id'])
    if duplicates.any():
        logger.warning(f'Found {duplicates.sum()} duplicate ratings')
        df_clean = df_clean.drop_duplicates(['user_id', 'book_id'])

    # verify rating values are in the expected range (1-5)
    invalid_ratings = ~df_clean['rating'].between(1, 5)
    if invalid_ratings.any():
        logger.warning(f'Found {invalid_ratings.sum()} invalid ratings outside the range 1-5')
        df_clean = df_clean[~invalid_ratings]

    # check for missing values
    if df_clean.isnull().any().any():
        logger.warning(f'Found missing values in ratings data')
        df_clean = df_clean.dropna()

    # ensure data types are correct
    df_clean['user_id'] = df_clean['user_id'].astype(int)
    df_clean['book_id'] = df_clean['book_id'].astype(int)
    df_clean['rating'] = df_clean['rating'].astype(int)

    logger.info(f'Ratings data cleaned: {len(df_clean)} records remaining')
    return df_clean

def clean_to_read(df):
    """Clean to-read data"""
    logger.info('Cleaning to-read data')

    df_clean = df.copy()

    # check for and remove duplicates
    duplicates = df_clean.duplicated(['user_id', 'book_id'])
    if duplicates.any():
        logger.warning(f'Found {duplicates.sum()} duplicate to-read entries')
        df_clean = df_clean.drop_duplicates(['user_id', 'book_id'])

    # check for missing values
    if df_clean.isnull().any().any():
        logger.warning(f'Found missing values in to-read data')
        df_clean = df_clean.dropna()

    # ensure data types are correct
    df_clean['user_id'] = df_clean['user_id'].astype(int)
    df_clean['book_id'] = df_clean['book_id'].astype(int)

    logger.info(f'To-read data cleaned: {len(df_clean)} records remaining')
    return df_clean

def clean_books(df):
    """Clean books data"""
    logger.info('Cleaning books data')

    df_clean = df.copy()

    # handle missing values
    # numeric - fill with appropriaate values or NaN
    # text - empty strings or appropriate placeholders

    # fix publication years
    # convert invalid years to NaN
    current_year = pd.Timestamp.now().year
    invalid_years = ~df_clean['original_publication_year'].between(0, current_year)
    if invalid_years.any():
        logger.warning(f'Found {invalid_years.sum()} invalid publication years')
        df_clean.loc[invalid_years, 'original_publication_year'] = np.nan

    # clean up text fields
    text_columns = ['title', 'authors', 'original_title']
    for col in text_columns:
        # replace NaN with empty string
        df_clean[col] = df_clean[col].fillna('')
        # strip whitespace
        df_clean[col] = df_clean[col].str.strip()

    # ensure ISBN is properly formatted
    df_clean['isbn'] = df_clean['isbn'].fillna('')
    # convert to string
    df_clean['isbn'] = df_clean['isbn'].astype(str)

    # ensure ISBN13 is properly formatted
    # fill missing with NaN
    df_clean['isbn13'] = pd.to_numeric(df_clean['isbn13'], errors='coerce')

    # ensure IDs are integers
    id_columns = ['book_id', 'goodreads_book_id', 'best_book_id', 'work_id']
    for col in id_columns:
        df_clean[col] = df_clean[col].astype(int)

    # check for duplicate book_id
    duplicates = df_clean.duplicated('book_id')
    if duplicates.any():
        logger.warning(f'Found {duplicates.sum()} duplicate book_id entries')
        df_clean = df_clean.drop_duplicates('book_id')

    logger.info(f'Books data cleaned: {len(df_clean)} records remaining')
    return df_clean

def clean_book_tags(df):
    """Clean book tags data"""
    logger.info('Cleaning book tags data')

    df_clean = df.copy()

    # check for missing values
    if df_clean.isnull().any().any():
        logger.warning(f'Found missing values in book tags data')
        df_clean = df_clean.dropna()

    # ensure data types are correct
    df_clean['goodreads_book_id'] = df_clean['goodreads_book_id'].astype(int)
    df_clean['tag_id'] = df_clean['tag_id'].astype(int)
    df_clean['count'] = df_clean['count'].astype(int)

    # check for duplicate goodreads_book_id/tag_id pairs
    duplicates = df_clean.duplicated(['goodreads_book_id', 'tag_id'])
    if duplicates.any():
        logger.warning(f'Found {duplicates.sum()} duplicate book tag entries')
        df_clean = df_clean.drop_duplicates(['goodreads_book_id', 'tag_id'])

    logger.info(f'Book tags data cleaned: {len(df_clean)} records remaining')
    return df_clean

def clean_tags(df):
    """Clean tags data"""
    logger.info('Cleaning tags data')

    df_clean = df.copy()

    # check for missing values
    if df_clean.isnull().any().any():
        logger.warning('Found missing values in tags data')
        df_clean = df_clean.dropna()

    # ensure data types are correct
    df_clean['tag_id'] = df_clean['tag_id'].astype(int)

    # clean tag names
    df_clean['tag_name'] = df_clean['tag_name'].str.strip().str.lower()

    # check for duplicate tag_id
    duplicates = df_clean.duplicated('tag_id')
    if duplicates.any():
        logger.warning(f'Found {duplicates.sum()} duplicate tag_id entries')
        df_clean = df_clean.drop_duplicates('tag_id')

    logger.info(f'Tags data cleaned: {len(df_clean)} records remaining')
    return df_clean

def transform_all(data_dict):
    """Clean all datasets"""
    transformed_data = {}

    transformed_data['ratings'] = clean_ratings(data_dict['ratings'])
    transformed_data['to_read'] = clean_to_read(data_dict['to_read'])
    transformed_data['books'] = clean_books(data_dict['books'])
    transformed_data['book_tags'] = clean_book_tags(data_dict['book_tags'])
    transformed_data['tags'] = clean_tags(data_dict['tags'])

    return transformed_data