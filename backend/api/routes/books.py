# backend/api/routes/books.py

"""
Book-related routes
"""

from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func, desc
import datetime

from database.models import Book, Rating, Tag, BookTag, User, UserActivity
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
        tag_name = request.args.get('tag_name', '', type=str)
        min_rating = request.args.get('min_rating', 0, type=float)
        max_rating = request.args.get('max_rating', 5, type=float)
        year_from = request.args.get('year_from', type=int)
        year_to = request.args.get('year_to', type=int)
        sort_by = request.args.get('sort_by', 'popularity', type=str)

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

        if max_rating < 5:
            query = query.filter(Book.average_rating <= max_rating)

        if year_from:
            query = query.filter(Book.original_publication_year >= year_from)
        
        if year_to:
            query = query.filter(Book.original_publication_year <= year_to)

        if tag_id:
            # join with book_tags to filter by tag
            query = query.join(BookTag, Book.goodreads_book_id == BookTag.goodreads_book_id) \
                         .filter(BookTag.tag_id == tag_id)
            
        if tag_name:
            # join with tags to filter by tag name
            query = query.join(BookTag, Book.goodreads_book_id == BookTag.goodreads_book_id) \
                         .join(Tag, BookTag.tag_id == Tag.tag_id) \
                         .filter(Tag.tag_name.ilike(f'%{tag_name}%'))
            
        # apply sorting
        if sort_by == 'title':
            query = query.order_by(Book.title)
        elif sort_by == 'author':
            query = query.order_by(Book.authors)
        elif sort_by == 'year':
            query = query.order_by(Book.original_publication_year.desc())
        elif sort_by == 'rating':
            query = query.order_by(Book.average_rating.desc())
        else:   # default: popularity
            query = query.order_by(Book.ratings_count.desc())

        # execute query with pagination
        books_page = query.paginate(page=page, per_page=per_page, error_out=False)

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
    
@books_bp.route('/tags', methods=['GET'])
def get_tags():
    """Get all tags with optional filtering"""
    try:
        # query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        name = request.args.get('name', '', type=str)
        sort_by = request.args.get('sort_by', 'popularity', type=str)

        # base query
        query = Tag.query

        # apply filters
        if name:
            query = query.filter(Tag.tag_name.ilike(f'%{name}%'))

        # apply sorting
        if sort_by == 'name':
            query = query.order_by(Tag.tag_name)
        else:   # default: popularity
            # subquery to count book_tags for each tag
            tag_counts = db.session.query(
                BookTag.tag_id,
                func.count(BookTag.goodreads_book_id).label('count')
            ).group_by(BookTag.tag_id).subquery()

            query = query.outerjoin(tag_counts, Tag.tag_id == tag_counts.c.tag_id) \
                         .order_by(desc(tag_counts.c.count))
            
        # execute with pagination
        tags_page = query.paginate(page=page, per_page=per_page, error_out=False)

        # get counts for each tag
        tag_ids = [tag.tag_id for tag in tags_page.items]
        tag_counts = db.session.query(
            BookTag.tag_id,
            func.count(BookTag.goodreads_book_id).label('count')
        ).filter(BookTag.tag_id.in_(tag_ids)) \
         .group_by(BookTag.tag_id).all()
        
        # create a dictionary for easy lookup
        counts_dict = {tag_id: count for tag_id, count in tag_counts}

        # format response
        tags_data = [{
            'tag_id': tag.tag_id,
            'tag_name': tag.tag_name,
            'book_count': counts_dict.get(tag.tag_id, 0)
        } for tag in tags_page.items]

        return success_response({
            'tags': tags_data,
            'pagination': {
                'total': tags_page.total,
                'pages': tags_page.pages,
                'current_page': tags_page.page,
                'per_page': tags_page.per_page,
                'has_next': tags_page.has_next,
                'has_prev': tags_page.has_prev
            }
        })
    
    except Exception as e:
        current_app.logger.error(f'Error getting tags: {str(e)}')
        return error_response('Failed to retrieve tags', 500)
    
@books_bp.route('/similar/<int:book_id>', methods=['GET'])
def get_similar_books(book_id):
    """Get books similar to the given book_id"""
    try:
        # get the book
        book = Book.query.get(book_id)
        if not book:
            return error_response('Book not found', 404)
        
        # get book tags
        book_tag_ids = db.session.query(BookTag.tag_id) \
                                 .filter(BookTag.goodreads_book_id == book.goodreads_book_id) \
                                 .all()
        book_tag_ids = [tag_id for (tag_id,) in book_tag_ids]

        if not book_tag_ids:
            # fallback if no tags found: get books by same author
            similar_books = Book.query \
                                .filter(Book.authors.ilike(f'%{book.authors}%')) \
                                .filter(Book.book_id != book_id) \
                                .order_by(Book.average_rating.desc()) \
                                .limit(10) \
                                .all()
        else:
            # find books with common tags
            similar_books_query = db.session.query(
                Book,
                func.count(BookTag.tag_id).label('tag_count')
            ).join(BookTag, Book.goodreads_book_id == BookTag.goodreads_book_id) \
             .filter(BookTag.tag_id.in_(book_tag_ids)) \
             .filter(Book.book_id != book_id) \
             .group_by(Book.book_id) \
             .order_by(desc('tag_count'), Book.average_rating.desc()) \
             .limit(10)
            
            similar_books = [book for book, _ in similar_books_query]

        # format response
        books_data = [{
            'book_id': book.book_id,
            'title': book.title,
            'authors': book.authors,
            'average_rating': book.average_rating,
            'ratings_count': book.ratings_count,
            'image_url': book.image_url,
            'publication_year': book.original_publication_year
        } for book in similar_books]

        return success_response(books_data)

    except Exception as e:
        current_app.logger.error(f'Error getting similar books: {str(e)}')
        return error_response('Failed to retrieve similar books', 500)
    
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
            'book_id': book.book_id,
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
    
@books_bp.route('/rate/<int:book_id>', methods=['PUT'])
@jwt_required()
def update_book_rating(book_id):
    """Update a book rating"""
    try:
        # get current user ID from JWT
        current_user = get_jwt_identity()
        user_id = current_user.get('user_id')

        # get JSON data from request
        data = request.get_json()

        # validate required fields
        if 'rating' not in data:
            return error_response('Rating is required', 400)
        
        rating_value = data['rating']
        review = data.get('review', '')

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
            # add/update review if provided
            if 'review' in data:
                existing_rating.review = review
            
            # add activity entry for rating update
            activity = UserActivity(
                user_id=user_id,
                activity_type='update_rating',
                book_id=book_id,
                details=f'Updated rating to {rating_value} stars'
            )
            db.session.add(activity)
            db.session.commit()

            return success_response({
                'rating': rating_value,
                'review': review
            }, 'Rating updated successfully')
        else:
            # create new rating
            new_rating = Rating(
                user_id=user_id,
                book_id=book_id,
                rating=rating_value,
                review=review if review else None,
                timestamp=datetime.datetime.now()
            )

            # add activity entry for new rating
            activity = UserActivity(
                user_id=user_id,
                activity_type='new_rating',
                book_id=book_id,
                details=f'Rated {rating_value} stars'
            )

            db.session.add(new_rating)
            db.session.add(activity)
            db.session.commit()

            return success_response({
                'rating': rating_value,
                'review': review
            }, 'Rating added successfully', 201)
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error updating book rating: {str(e)}')
        return error_response('Failed to update rating', 500)
    
@books_bp.route('/reviews/<int:book_id>', methods=['GET'])
def get_book_reviews(book_id):
    """Get reviews for a specific book"""
    try:
        # get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        # check if book exists
        book = Book.query.get(book_id)
        if not book:
            return error_response('Book not found', 404)
        
        # get ratings with reviews
        reviews_page = db.session.query(Rating, User) \
                                 .join(User, Rating.user_id == User.user_id) \
                                 .filter(Rating.book_id == book_id) \
                                 .filter(Rating.review.isnot(None)) \
                                 .filter(Rating.review != '') \
                                 .order_by(Rating.timestamp.desc()) \
                                 .paginate(page=page, per_page=per_page, error_out=False)
        
        # format response
        reviews_data = [{
            'user_id': user.user_id,
            'username': user.username,
            'rating': rating.rating,
            'review': rating.review,
            'timestamp': rating.timestamp.isoformat() if rating.timestamp else None
        } for rating, user in reviews_page.items]

        return success_response({
            'reviews': reviews_data,
            'pagination': {
                'total': reviews_page.total,
                'pages': reviews_page.pages,
                'current_page': reviews_page.page,
                'per_page': reviews_page.per_page,
                'has_next': reviews_page.has_next,
                'has_prev': reviews_page.has_prev
            }
        })
    
    except Exception as e:
        current_app.logger.error(f'Error getting book reviews: {str(e)}')
        return error_response('Failed to retrieve reviews', 500)