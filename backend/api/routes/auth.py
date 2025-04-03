# backend/api/routs/auth.py

"""
Authentication routes
"""

from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

from database.models import User
from backend.app import db
from backend.api.utils.responses import success_response, error_response
from backend.api.utils.auth import hash_password, check_password, generate_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        # get JSON data from request
        data = request.get_json()

        # validate required fields
        if not all(k in data for k in ('username', 'email', 'password')):
            return error_response('Missing required fields', 400)
        
        # check if username or email already exists
        existing_user = User.query.filter(
            (User.username == data['username']) |
            (User.email == data['email'])
        ).first()

        if existing_user:
            return error_response('Username or email already exists', 409)
        
        # create new user
        new_user = User(
            username=data['username'],
            email=data['email'],
            password_hash=hash_password(data['password'])
        )

        # add to database
        db.session.add(new_user)
        db.session.commit()

        # generate token
        token = generate_token(new_user.user_id)

        return success_response({
            'user_id': new_user.user_id,
            'username': new_user.username,
            'token': token
        }, 'User registered successfully', 201)
    
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error in user registration: {str(e)}')
        return error_response('Registration failed', 500)
    
@auth_bp.route('/login', methods=['POST'])
def login():
    """Authenticate a user and return a token"""
    try:
        # get JSON data from request
        data = request.get_json()

        # validate required fields
        if not all(k in data for k in ('username', 'password')):
            return error_response('Missing username or password', 400)
        
        # find user by username
        user = User.query.filter_by(username=data['username']).first()

        # check if user exists and password is correct
        if not user or not check_password(user.password_hash, data['password']):
            return error_response('Invalid username or password', 401)
        
        # generate token
        token = generate_token(user.user_id)

        return success_response({
            'user_id': user.user_id,
            'username': user.username,
            'token': token
        }, 'Login successful')
    
    except Exception as e:
        current_app.logger.error(f'Error in user login: {str(e)}')
        return error_response('Login failed', 500)
    
@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current user information"""
    try:
        # get current user ID from JWT
        current_user = get_jwt_identity()
        user_id = current_user.get('user_id')

        # get user from database
        user = User.query.get(user_id)

        if not user:
            return error_response('User not found', 404)
        
        return success_response({
            'user_id': user.user_id,
            'username': user.username,
            'email': user.email,
            'joined_date': user.joined_date.isoformat() if user.joined_date else None,
            'profile_image': user.profile_image
        })
    
    except Exception as e:
        current_app.logger.error(f'Error getting current user: {str(e)}')
        return error_response('Failed to get user information', 500)