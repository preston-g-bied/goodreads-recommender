# check_environment.py

"""
Check and set up the environment for the Goodbooks application
Run this script before starting the application to ensure all directories exist.
"""

import os
from pathlib import Path

def setup_environment():
    """Set up the environment for the Goodbooks application"""
    # get the project root directory
    project_root = Path(__file__).resolve().parent
    
    # define required directories
    required_dirs = [
        project_root / "database",
        project_root / "logs",
        project_root / "data" / "raw",
        project_root / "data" / "processed"
    ]
    
    # create directories if they don't exist
    for directory in required_dirs:
        if not directory.exists():
            print(f"Creating directory: {directory}")
            directory.mkdir(parents=True, exist_ok=True)
    
    # check for database file
    database_path = project_root / "database" / "goodbooks.db"
    if not database_path.exists():
        print(f"Database file does not exist at: {database_path}")
        print("Note: The database file will be created when the application runs.")
        print("      If you have an existing database, place it at the above location.")
    else:
        print(f"Database file found at: {database_path}")
    
    print("\nEnvironment setup complete!")
    print(f"Project root: {project_root}")
    
    return True

if __name__ == "__main__":
    print("Setting up environment for Goodbooks application...")
    setup_environment()