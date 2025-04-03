# backend/api/routes/books.py

"""
Book-related routes
"""

from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func, desc

from database.models import Book, Rating, Tag, BookTag
from backend.app import db
from backend.api.utils.responses import success_response, error_response

books_bp = Blueprint('books', __name__)

@books_bp.route('/', methods=['GET'])
def get_books():
    """Get list of books with optional filtering and pagination"""
    try:
        # get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        title = request.args.get('title', '', type=str)
        author = request.args.get('author', '', type=str)
        tag_id = request.args.get('tag_id', type=int)
        min_rating = request.args.get('min_rating', 0, type=float)

        # limit page size
        per_page = min(per_page, 100)

        # base query
        query = Book.query

        # apply filters
        if title:
            query = query.filter(Book.title.ilike(f'%{title}%'))

        if author:
            query = query.filter(Book.authors.ilike(f'%{author}%'))

        if min_rating > 0:
            query = query.filter(Book.average_rating >= min_rating)

        if tag_id:
            # join with book_tags to filter by tag
            query = query.join(BookTag, Book.goodreads_book_id == BookTag.goodreads_book_id) \
                         .filter(BookTag.tag_id == tag_id)

        # execute query with pagination
        books_page = query.order_by(Book.average_rating.desc()) \
                          .paginate(page=page, per_page=per_page, error_out=False)

        # format response
        books_data = [{
            'book_id': book.book_id,
            'title': book.title,
            'authors': book.authors,
            'average_rating': book.average_rating,
            'ratings_count': book.ratings_count,
            'image_url': book.image_url,
            'publication_year': book.original_publication_year
        } for book in books_page.items]

        return success_response({
            'books': books_data,
            'pagination': {
                'total': books_page.total,
                'pages': books_page.pages,
                'current_page': books_page.page,
                'per_page': books_page.per_page,
                'has_next': books_page.has_next,
                'has_prev': books_page.has_prev
            }
        })
    
    except Exception as e:
        current_app.logger.error(f'Error getting books: {str(e)}')
        return error_response('Failed to retrieve books', 500)
    
@books_bp.route('/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """Get a specific book by ID"""
    try:
        # get book from database
        book = Book.query.get(book_id)

        if not book:
            return error_response('Book not found', 404)
        
        # get book tags
        book_tags = db.session.query(Tag.tag_name, BookTag.count) \
                              .join(BookTag, Tag.tag_id == BookTag.tag_id) \
                              .filter(BookTag.goodreads_book_id == book.goodreads_book_id) \
                              .order_by(BookTag.count.desc()) \
                              .limit(10) \
                              .all()
        
        # format response
        book_data = {
            'book_id': book.bool_id,
            'goodreads_book_id': book.goodreads_book_id,
            'work_id': book.work_id,
            'title': book.title,
            'authors': book.authors,
            'original_title': book.original_title,
            'original_publication_year': book.original_publication_year,
            'language_code': book.language_code,
            'average_rating': book.average_rating,
            'ratings_count': book.ratings_count,
            'ratings_distribution': {
                '1_star': book.ratings_1,
                '2_star': book.ratings_2,
                '3_star': book.ratings_3,
                '4_star': book.ratings_4,
                '5_star': book.ratings_5
            },
            'image_url': book.image_url,
            'small_image_url': book.small_image_url,
            'isbn': book.isbn,
            'isbn13': book.isbn13,
            'tags': [{'name': tag[0], 'count': tag[1]} for tag in book_tags]
        }

        return success_response(book_data)
    
    except Exception as e:
        current_app.logger.error(f'Error getting book: {str(e)}')
        return error_response('Failed to retrieve book', 500)
    
@books_bp.route('/popular', methods=['GET'])
def get_popular_books():
    """Get popular books based on ratings count"""
    try:
        # get query parameters
        limit = request.args.get('limit', 10, type=int)
        limit = min(limit, 50)  # cap at 50

        # query books ordered by ratings count
        popular_books = Book.query.order_by(Book.ratings_count.desc()).limit(limit).all()

        # format response
        books_data = [{
            'book_id': book.book_id,
            'title': book.title,
            'authors': book.authors,
            'average_rating': book.average_rating,
            'ratings_count': book.ratings_count,
            'image_url': book.image_url,
            'publication_year': book.original_publication_year
        } for book in popular_books]

        return success_response(books_data)
    
    except Exception as e:
        current_app.logger.error(f'Error getting popular books: {str(e)}')
        return error_response('Failed to retrieve popular books', 500)
    
@books_bp.route('/rate', methods=['POST'])
@jwt_required()
def rate_book():
    """Rate a book (requires authentication)"""
    try:
        # get current user ID from JWT
        current_user = get_jwt_identity()
        user_id = current_user.get('user_id')

        # get JSON data from request
        data = request.get_json()

        # validate all required fields
        if not all(k in data for k in ('book_id', 'rating')):
            return error_response('Missing required fields', 400)
        
        book_id = data['book_id']
        rating_value = data['rating']

        # validate rating value
        if not isinstance(rating_value, int) or rating_value < 1 or rating_value > 5:
            return error_response('Rating must be an integer between 1 and 5', 400)
        
        # check if book exists
        book = Book.query.get(book_id)
        if not book:
            return error_response('Book not found', 404)
        
        # check if rating already exists
        existing_rating = Rating.query.filter_by(
            user_id=user_id,
            book_id=book_id
        ).first()

        if existing_rating:
            # update existing rating
            existing_rating.rating = rating_value
            db.session.commit()
            return success_response({'rating': rating_value}, 'Rating updated successfully')
        else:
            # create new rating
            new_rating = Rating(
                user_id=user_id,
                book_id=book_id,
                rating=rating_value
            )
            db.session.add(new_rating)
            db.session.commit()
            return success_response({'rating': rating_value}, 'Rating added successfully', 201)
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error rating book: {str(e)}')
        return error_response('Failed to rate book', 500)
    
@books_bp.route('/search', methods=['GET'])
def search_books():
    """Search books by title, author, or tag"""
    try:
        # get query parameters
        query = request.args.get('q', '', type=str)
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)

        if not query:
            return error_response('Search query is required', 400)
        
        # limit page size
        per_page = min(per_page, 100)

        # search in title and author
        search_results = Book.query.filter(
            (Book.title.ilike(f'%{query}%')) |
            (Book.authors.ilike(f'%{query}%'))
        ).order_by(
            Book.ratings_count.desc()
        ).paginate(page=page, per_page=per_page, error_out=False)

        # format response
        books_data = [{
            'book_id': book.book_id,
            'title': book.title,
            'authors': book.authors,
            'average_rating': book.average_rating,
            'ratings_count': book.ratings_count,
            'image_url': book.image_url,
            'publication_year': book.original_publication_year
        } for book in search_results.items]

        return success_response({
            'books': books_data,
            'pagination': {
                'total': search_results.total,
                'pages': search_results.pages,
                'current_page': search_results.page,
                'per_page': search_results.per_page,
                'has_next': search_results.has_next,
                'has_prev': search_results.has_prev
            }
        })
    
    except Exception as e:
        current_app.logger.error(f'Error searching books: {str(e)}')
        return error_response('Failed to search books', 500)