# database/migrations/create_migrations.py

import sys
from pathlib import Path
import os
import sqlite3
import logging
from datetime import datetime

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from database.models import create_tables
from backend.config import config

# set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger('migrations')

def create_migrations_table(conn):
    """Create migrations tracking table if it doesn't exist"""
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS migrations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        applied_at TIMESTAMP NOT NULL
    )
    ''')
    conn.commit()

def get_applied_migrations(conn):
    """Get a list of already applied migrations"""
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM migrations')
    return [row[0] for row in cursor.fetchall()]

def apply_migration(conn, migration_name, migration_function):
    """Apply a single migration and record it"""
    try:
        migration_function(conn)

        # record the migration
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO migrations (name, applied_at) VALUES (?, ?)',
            (migration_name, datetime.now().isoformat())
        )
        conn.commit()
        logger.info(f'Applied migration: {migration_name}')
        return True
    except Exception as e:
        conn.rollback()
        logger.error(f'Failed to apply migration {migration_name}: {e}')
        return False
    
def add_review_to_ratings(conn):
    """Migration to add review column to ratings table"""
    cursor = conn.cursor()
    cursor.execute('ALTER TABLE ratings ADD COLUMN review TEXT')
    conn.commit()

def run_migrations():
    """Run all pending migrations"""
    # get database path from config
    db_path = config.SQLALCHEMY_DATABASE_URI.replace('sqlite:///', '')

    # create parent directory if it doesn't exist
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    # connect to database
    conn = sqlite3.connect(db_path)

    # create migrations table
    create_migrations_table(conn)

    # get already applied migrations
    applied_migrations = get_applied_migrations(conn)

    # list of migrations to apply
    migrations = [
        ('add_review_to_ratings', add_review_to_ratings)
    ]

    # apply pending migrations
    success = True
    for name, func in migrations:
        if name not in applied_migrations:
            logger.info(f'Applying migration: {name}')
            if not apply_migration(conn, name, func):
                success = False
                break
        else:
            logger.info(f'Migration already applied: {name}')

    # close connection
    conn.close()
    return success

if __name__ == '__main__':
    logger.info('Starting database migrations...')
    if run_migrations():
        logger.info('Migrations completed successfully')
    else:
        logger.error('Migrations failed')
        sys.exit(1)