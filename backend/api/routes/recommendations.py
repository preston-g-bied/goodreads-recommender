# backend/api/routes/recommendations.py

from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func, desc
import datetime

from database.models import Book, Rating, Tag, BookTag, User, UserActivity, Recommendation
from backend.app import db
from backend.api.utils.responses import success_response, error_response

recommendations_bp = Blueprint('recommendations', __name__)

@recommendations_bp.route('/popular', methods=['GET'])
def get_popular_recommendations():
    """Get popular book recommendations"""
    try:
        # get query parameters
        limit = request.args.get('limit', 10, type=int)
        exclude_rated = request.args.get('exclude_rated', 'false', type=str).lower() == 'true'
        user_id = None

        # check if user is authenticated
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.statswith('Bearer '):
            from flask_jwt_extended import decode_token
            try:
                token = auth_header.split('Bearer ')[1]
                token_data = decode_token(token)
                user_id = token_data['sub']['user_id']
            except Exception as e:
                current_app.logger.warning(f'Failed to decode token: {str(e)}')

        # base query
        query = db.session.query(Book) \
                          .filter(Book.ratings_count > 100) \
                          .order_by(Book.average_rating.desc(), Book.ratings_count.desc())
        
        # exclude books the user has already rated if requested
        if exclude_rated and user_id:
            rated_books = db.session.query(Rating.book_id) \
                                    .filter(Rating.user_id == user_id) \
                                    .subquery()
            query = query.filter(~Book.book_id.in_(rated_books))

        # execute query
        popular_books = query.limit(limit).all()

        # format response
        books_data = [{
            'book_id': book.book_id,
            'title': book.title,
            'authors': book.authors,
            'average_rating': book.average_rating,
            'ratings_count': book.ratings_count,
            'image_url': book.image_url,
            'publication_year': book.original_publication_year,
            'language_code': book.language_code
        } for book in popular_books]

        return success_response(books_data)
    
    except Exception as e:
        current_app.logger.error(f'Error getting popular recommendations: {str(e)}')
        return error_response('Failed to retrieve recommendations', 500)
    
@recommendations_bp.route('/personalized', methods=['GET'])
@jwt_required()
def get_personalized_recommendations():
    """Get personalized book recommendations based on user's ratings"""
    try:
        # get current user ID from JWT
        current_user = get_jwt_identity()
        user_id = current_user.get('user_id')

        # get query parameters
        limit = request.args.get('limit', 10, type=int)

        # check if user has ratings
        user_ratings_count = db.session.query(func.count(Rating.book_id)) \
                                       .filter(Rating.user_id == user_id) \
                                       .scalar()
        
        if user_ratings_count == 0:
            # fallback to popular recommendations if user has no ratings
            return get_popular_recommendations()
        
        # get the tags of books the user has rated highly (4 or 5 stars)
        liked_tags = db.session.query(
            Tag.tag_id,
            Tag.tag_name,
            func.count(Tag.tag_id).label('count')
        ).join(BookTag, Tag.tag_id == BookTag.tag_id) \
         .join(Book, BookTag.goodreads_book_id == Book.goodreads_book_id) \
         .join(Rating, Rating.book_id == Book.book_id) \
         .filter(Rating.user_id == user_id) \
         .filter(Rating.rating >= 4) \
         .group_by(Tag.tag_id, Tag.tag_name) \
         .order_by(desc('count')) \
         .limit(5) \
         .all()
        
        if not liked_tags:
            # fallback to popular recommendations if no liked tags found
            return get_popular_recommendations()
        
        # get tag IDs
        tag_ids = [tag_id for tag_id, _, _ in liked_tags]

        # get books with these tags that the user hasn't rated yet
        rated_books = db.session.query(Rating.book_id) \
                                .filter(Rating.user_id == user_id) \
                                .subquery()
        
        recommended_books = db.session.query(
            Book,
            func.count(BookTag.tag_id).label('tag_count')
        ).join(BookTag, Book.goodreads_book_id == BookTag.goodreads_book_id) \
         .filter(BookTag.tag_id.in_(tag_ids)) \
         .filter(~Book.book_id.in_(rated_books)) \
         .filter(Book.average_rating >= 3.5) \
         .filter(Book.ratings_count >= 50) \
         .group_by(Book.book_id) \
         .order_by(desc('tag_count'), Book.average_rating.desc()) \
         .limit(limit) \
         .all()
        
        # format response
        books_data = [{
            'book_id': book.book_id,
            'title': book.title,
            'authors': book.authors,
            'average_rating': book.average_rating,
            'ratings_count': book.ratings_count,
            'image_url': book.image_url,
            'publication_year': book.original_publication_year,
            'language_code': book.language_code,
            'reason': 'Based on your taste in books'
        } for book, _ in recommended_books]

        # store recommendations for tracking
        timestamp = datetime.datetime.now()
        for book, _ in recommended_books:
            new_recommendation = Recommendation(
                user_id=user_id,
                book_id=book.book_id,
                source='tag_based',
                generated_at=timestamp,
                score=book.average_rating
            )
            db.session.add(new_recommendation)

        db.session.commit()

        return success_response(books_data)
    
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error getting personalized recommendations: {str(e)}')
        return error_response('Failed to retrieve recommendations', 500)