# backed/api/utils/auth.py

"""
Authentication utilities for the API
"""

from flask_jwt_extended import create_access_token, get_jwt_identity, verify_jwt_in_request
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask import request, current_app

from backend.api.utils.responses import error_response

def hash_password(password):
    """Generate a secure hash of the password"""
    return generate_password_hash(password)

def check_password(password_hash, password):
    """Check if the password matches the hash"""
    return check_password_hash(password_hash, password)

def generate_token(user_id):
    """Generate an access token for the user"""
    identity = {'user_id': user_id}
    return create_access_token(identity=identity)

def get_current_user_id():
    """Get the current authenticated user ID from the JWT"""
    current_user = get_jwt_identity()
    return current_user.get('user_id') if current_user else None

def admin_required(fn):
    """Decorator to check if user is an admin"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # first verify the JWT is valid
        verify_jwt_in_request()

        # get the current user ID
        user_id = get_current_user_id()

        # check if user is admin (in real app, would query the database)
        # for now, assume user ID 1 is admin
        if user_id != 1:
            return error_response('Admin privledges required', 403)
        
        return fn(*args, **kwargs)
    
    return wrapper