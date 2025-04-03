# backend/api/routes/users.py

"""
User-related routes
"""

from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

from database.models import User, Rating, Book, ToRead
from backend.app import db
from backend.api.utils.responses import success_response, error_response
from backend.api.utils.auth import hash_password, check_password

users_bp = Blueprint('users', __name__)

@users_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user's profile"""
    try:
        # get current user ID from JWT
        current_user = get_jwt_identity()
        user_id = current_user.get('user_id')

        # get user from database
        user = User.query.get(user_id)

        if not user:
            return error_response('User not found', 404)
        
        # get user's ratings
        ratings_count = Rating.query.filter_by(user_id=user_id).count()

        # get user's to-read list count
        to_read_count = ToRead.query.filter_by(user_id=user_id).count()

        return success_response({
            'user_id': user.user_id,
            'username': user.username,
            'email': user.email,
            'joined_date': user.joined_date.isoformat() if user.joined_date else None,
            'profile_image': user.profile_image,
            'stats': {
                'ratings_count': ratings_count,
                'to_read_count': to_read_count
            }
        })
    
    except Exception as e:
        current_app.logger.error(f'Error getting user profile: {str(e)}')
        return error_response('Failed to retrieve profile', 500)
    
@users_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update current user's profile"""
    try:
        # get current user ID from JWT
        current_user = get_jwt_identity()
        user_id = current_user.get('user_id')

        # get user from database
        user = User.query.get(user_id)

        if not user:
            return error_response('User not found', 404)
        
        # get JSON data from request
        data = request.get_json()

        # update user fields if provided
        if 'username' in data:
            # check if username is already taken
            existing_user = User.query.filter(
                User.username == data['username'],
                User.user_id != user_id
            ).first()

            if existing_user:
                return error_response('Username already taken', 409)
            
            user.username = data['username']

        if 'email' in data:
            # check if email is already taken
            existing_user = User.query.filter(
                User.email == data['email'],
                User.user_id != user_id
            ).first()

            if existing_user:
                return error_response('Email already taken', 409)

            user.email = data['email']

        if 'profile_image' in data:
            user.profile_image = data['profile_image']

        # update password if provided
        if 'password' in data and 'current_password' in data:
            # verify current password
            if not check_password(user.password_hash, data['current_password']):
                return error_response('Current password is incorrect', 401)

            # update password
            user.password_hash = hash_password(data['password'])

        # save changes
        db.session.commit()

        return success_response({
            'user_id': user.user_id,
            'username': user.username,
            'email': user.email,
            'profile_image': user.profile_image
        }, 'Profile updated successfully')

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error updating user profile: {str(e)}')
        return error_response('Failed to update profile', 500)

@users_bp.route('/ratings', methods=['GET'])
@jwt_required()
def get_user_ratings():
    """Get current user's book ratings"""
    try:
        # Get current user ID from JWT
        current_user = get_jwt_identity()
        user_id = current_user.get('user_id')

        # get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)

        # limit page size
        per_page = min(per_page, 100)

        # get user's ratings with book information
        ratings_page = db.session.query(Rating, Book) \
                         .join(Book, Rating.book_id == Book.book_id) \
                         .filter(Rating.user_id == user_id) \
                         .order_by(Rating.timestamp.desc()) \
                         .paginate(page=page, per_page=per_page, error_out=False)
        
        # format response
        ratings_data = [{
            'book_id': book.book_id,
            'title': book.title,
            'authors': book.authors,
            'rating': rating.rating,
            'image_url': book.image_url,
            'timestamp': rating.timestamp.isoformat() if rating.timestamp else None
        } for rating, book in ratings_page.items]

        return success_response({
            'ratings': ratings_data,
            'pagination': {
                'total': ratings_page.total,
                'pages': ratings_page.pages,
                'current_page': ratings_page.page,
                'per_page': ratings_page.per_page,
                'has_next': ratings_page.has_next,
                'has_prev': ratings_page.has_prev
            }
        })

    except Exception as e:
        current_app.logger.error(f'Error getting user ratings: {str(e)}')
        return error_response('Failed to retrieve ratings', 500)

@users_bp.route('/to-read', methods=['GET'])
@jwt_required()
def get_to_read_list():
    """Get current user's to-read list"""
    try:
        # get current user ID from JWT
        current_user = get_jwt_identity()
        user_id = current_user.get('user_id')
        
        # get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # limit page size
        per_page = min(per_page, 100)

        # get user's to-read list with book information
        to_read_page = db.session.query(ToRead, Book) \
                         .join(Book, ToRead.book_id == Book.book_id) \
                         .filter(ToRead.user_id == user_id) \
                         .order_by(ToRead.added_date.desc()) \
                         .paginate(page=page, per_page=per_page, error_out=False)
        
        # format response
        to_read_data = [{
            'book_id': book.book_id,
            'title': book.title,
            'authors': book.authors,
            'average_rating': book.average_rating,
            'image_url': book.image_url,
            'added_date': to_read.added_date.isoformat() if to_read.added_date else None
        } for to_read, book in to_read_page.items]
        
        return success_response({
            'to_read': to_read_data,
            'pagination': {
                'total': to_read_page.total,
                'pages': to_read_page.pages,
                'current_page': to_read_page.page,
                'per_page': to_read_page.per_page,
                'has_next': to_read_page.has_next,
                'has_prev': to_read_page.has_prev
            }
        })
        
    except Exception as e:
        current_app.logger.error(f'Error getting to-read list: {str(e)}')
        return error_response('Failed to retrieve to-read list', 500)
    
@users_bp.route('/to-read/<int:book_id>', methods=['POST'])
@jwt_required()
def add_to_read(book_id):
    """Add a book to user's to-read list"""
    try:
        # get current user ID from JWT
        current_user = get_jwt_identity()
        user_id = current_user.get('user_id')

        # check if book exists
        book = Book.query.get(book_id)
        if not book:
            return error_response('Book not found', 404)
        
        # check if book is already in to-read list
        existing_to_read = ToRead.query.filter_by(
            user_id=user_id,
            book_id=book_id
        ).first()

        if existing_to_read:
            return error_response('Book already in to-read list', 409)
        
        # add book to to-read list
        new_to_read = ToRead(
            user_id=user_id,
            book_id=book_id
        )
        db.session.add(new_to_read)
        db.session.commit()

        return success_response({
            'book_id': book_id,
            'title': book.title
        }, 'Book added to to-read list', 201)
    
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error adding book to to-read list: {str(e)}')
        return error_response('Failed to add book to to-read list', 500)
    
@users_bp.route('/to-read/<int:book_id>', methods=['DELETE'])
@jwt_required()
def remove_from_to_read(book_id):
    """Remove a book from the user's to-read list"""
    try:
        # get a current user ID from JWT
        current_user = get_jwt_identity()
        user_id = current_user.get('user_id')

        # find to-read entry
        to_read = ToRead.query.filter_by(
            user_id=user_id,
            book_id=book_id
        ).first()

        if not to_read:
            return error_response('Book not in to-read list', 404)
        
        # remove from to-read list
        db.session.delete(to_read)
        db.session.commit()

        return success_response(message='Book removed from to-read list')
    
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error removing from to-read list: {str(e)}')
        return error_response('Failed to remove book from to-read list', 500)