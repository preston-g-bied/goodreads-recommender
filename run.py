# run.py

"""
Run script for the Goodbooks API
"""

import sys
from pathlib import Path
import os

sys.path.append(str(Path(__file__).resolve().parent))

# import and run environment setup
from check_environment import setup_environment
setup_environment()

# set Flask environment variables
os.environ['FLASK_APP'] = 'backend/app.py'
os.environ['FLASK_ENV'] = 'development'

from backend.app import create_app

if __name__ == '__main__':
    print('Starting Goodbooks API...')
    app = create_app()
    print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    app.run(debug=True, host='0.0.0.0', port=5000)