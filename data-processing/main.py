# data-processing/main.py

"""
Main ETL script to orchestrate the extract, transform, and load processes
"""

import logging
import argparse
from pathlib import Path
import sys
import time

# import ETL modules
from etl.extract import extract_all
from etl.transform import transform_all
from etl.load import save_to_csv, load_to_database
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

def run_etl_pipeline(load_to_db=True, save_csv=True):
    """
    Run the complete ETL pipeline

    Args:
        load_to_db (bool): Whether to load data to database
        save_csv (bool): Whether to save cleaned data as CSV
    """
    start_time = time.time()
    logger.info('Starting ETL pipeline')

    try:
        # extract
        logger.info('Starting data extraction')
        raw_data = extract_all()
        logger.info('Data extraction completed')

        # transform
        logger.info('Starting data transformation')
        transformed_data = transform_all(raw_data)
        logger.info('Data transformation completed')

        # load
        if save_csv:
            logger.info('Saving data to CSV')
            save_to_csv(transformed_data)
            logger.info('Data saved to CSV')

        if load_to_db:
            logger.info('Loading data to database')
            load_to_database(transformed_data)
            logger.info('Data loaded to database')

        elapsed_time = time.time() - start_time
        logger.info(f'ETL pipeline completed successfully in {elapsed_time:.2f} seconds')
        return True
    
    except Exception as e:
        logger.error(f'ETL pipeline failed: {e}')
        elapsed_time = time.time() - start_time
        logger.info(f'ETL pipeline failed after {elapsed_time:.2f} seconds')
        return False
    
if __name__ == '__main__':
    # parse command line arguments
    parser = argparse.ArgumentParser(description='Run the Goodbooks-10k ETL pipeline')
    parser.add_argument('--no-db', action='store_false', dest='load_to_db',
                        help='Skip loading data to database')
    parser.add_argument('--no-csv', action='store_false', dest='save_csv',
                        help='Skip saving data as CSV')
    args = parser.parse_args()

    # run the ETL pipeline
    success = run_etl_pipeline(load_to_db=args.load_to_db, save_csv=args.save_csv)

    # exit with appropriate status code
    sys.exit(0 if success else 1)