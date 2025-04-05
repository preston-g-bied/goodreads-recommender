// frontend/goodbooks-client/src/components/books/BookDetailsPage.js

import React, {useState, useEffect } from 'react';
import {useParams, Link } from 'react-router-dom';
import {
    getBookById,
    getSimilarBooks,
    getBookReviews,
    rateBook
} from '../../services/bookService';
import { addToReadingList, removeFromReadingList } from '../../services/userService';
import { useAuth } from '../../context/AuthContext';
import BookCard from '../common/BookCard';
import StarRating from '../common/StarRating';
import './BookDetailsPage.css'

const BookDetailsPage = () => {
    const { bookId } = useParams();
    const { isAuthenticated } = useAuth();
    const [book, setBook] = useState(null);
    const [similarBooks, setSimilarBooks] = useState([]);
    const [reviews, setReviews] = useState([]);
    const [userRating, setUserRating] = useState(0);
    const [userReview, setUserReview] = useState('');
    const [inReadingList, setInReadingList] = useState(false);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [successMessage, setSuccessMessage] = useState('');

    useEffect(() => {
        const fetchBookData = async () => {
            try {
                setLoading(true);
                setError(null);

                // fetch book details
                const bookResponse = await getBookById(bookId);
                if (bookResponse.success) {
                    setBook(bookResponse.data);
                }

                // fetch similar books
                const similarResponse = await getSimilarBooks(bookId);
                if (similarResponse.success) {
                    getSimilarBooks(similarResponse.data);
                }

                // fetch book reviews
                const reviewsResponse = await getBookReviews(bookId);
                if (reviewsResponse.success) {
                    setReviews(reviewsResponse.data.reviews);
                }

                // if authenticated, check if book is in reading list
                if (isAuthenticated) {
                    // this could be implemented by checking the user's reading list
                    // or by adding an endpoint to check if a specific book is in the list
                    // for now, assume it's not in the list
                    setInReadingList(false);
                }
            } catch (err) {
                console.error(`Error fetching book data for book ${bookId}:`, err);
                setError('Failed to load book data. Please try again later.');
            } finally {
                setLoading(false)
            }
        };

        fetchBookData();
    }, [bookId, isAuthenticated]);

    const handleRatingChange = (rating) => {
        setUserRating(rating);
    };

    const handleReviewChange = (e) => {
        setUserReview(e.target.value);
    };

    const handleSubmitRating = async (e) => {
        e.preventDefault();
        if (!isAuthenticated) {
            return;
        }

        try {
            const response = await rateBook(bookId, userRating, userReview);
            if (response.success) {
                setSuccessMessage('Rating submitted successfully!');
                setTimeout(() => setSuccessMessage(''), 3000);
            }
        } catch (err) {
            setError('Failed to submit rating. Please try again.');
            setTimeout(() => setError(''), 3000);
        }
    };

    const handleReadingListToggle = async () => {
        if (!isAuthenticated) {
            return;
        }

        try {
            if (inReadingList) {
                await removeFromReadingList(bookId);
                setInReadingList(false);
                setSuccessMessage('Removed from reading list');
            } else {
                await addToReadingList(bookId);
                setInReadingList(true);
                setSuccessMessage('Added to reading list');
            }
            setTimeout(() => setSuccessMessage(''), 3000);
        } catch (err) {
            setError('Failed to update reading list. Please try agian.')
            setTimeout(() => setError(), 3000);
        }
    };

    if (loading) {
        return <div className="loading">Loading...</div>;
    }

    if (error) {
        return <div className="error-message">{error}</div>;
    }

    if (!book) {
        return <div className="error-message">Book not found</div>;
    }

    return (
        <div className="book-detail-page">
            {/* Breadcrumb Navigation */}
            <div className="breadcrumb">
                <Link to="/">Home</Link> &gt;
                <Link to="/search">Browse</Link> &gt;
                <span>{book.title}</span>
            </div>

            {successMessage && (
                <div className="success-message">{successMessage}</div>
            )}

            {/* Book Detail Section */}
            <div className="book-detail">
                {/* Book Cover */}
                <div className="book-detail-cover">
                    {book.image_url ? (
                        <img src={book.image_url} alt={`Cover of ${book.title}`} />
                    ) : (
                        <div className="book-cover-placeholder">No Cover Available</div>
                    )}
                </div>

                {/* Book Information */}
                <div className="book-detail-info">
                    <h1>{book.title}</h1>
                    <div className="book-detail-meta">
                        <p>
                            By <Link to={`/search?author=${encodeURIComponent(book.authors)}`}>{book.authors}</Link>
                            {book.original_publication_year && ` | Published in ${book.original_publication_year}`}
                        </p>
                        <p>
                            <span className="rating-stars">
                                {/* Display rating stars */}
                                {Array.from({ length: 5 }, (_, i) => (
                                    <span key={i} className={i < Math.floor(book.average_rating) ? "star full" : "star empty"}>
                                        {i < Math.floor(book.average_rating) ? "★" : "☆"}
                                    </span>
                                ))}
                            </span>
                            <span className="rating-value">{book.average_rating.toFixed(1)}</span> ·
                            <span className="rating-count">{book.ratings_count} ratings</span>
                        </p>
                    </div>

                    {/* Book Actions */}
                    <div className="book-actions">
                        {isAuthenticated && (
                            <>
                                <button
                                    className={`btn ${inReadingList ? 'btn-secondary' : 'btn-primary'}`}
                                    onClick={handleReadingListToggle}
                                >
                                    {inReadingList ? 'Remove from Reading List' : 'Add to Reading List'}
                                </button>
                            </>
                        )}
                    </div>

                    {/* Book Tags */}
                    {book.tags && book.tags.length > 0 && (
                        <div className="book-tags">
                            <h3>Tags</h3>
                            <ul className="tags-list">
                                {book.tags.map((tag, index) => (
                                    <li key={index} className="tag-item">
                                        <Link
                                            to={`/search?tag_name=${encodeURIComponent(tag.name)}`}
                                            className="tag-link"
                                        >
                                            {tag.name}
                                        </Link>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    )}

                    {/* Book Details */}
                    <div className="book-details-section">
                        <h3>Details</h3>
                        <table className="book-details-table">
                            {book.isbn && (
                                <tr>
                                    <td><strong>ISBN:</strong></td>
                                    <td>{book.isbn}</td>
                                </tr>
                            )}
                            {book.language_code && (
                                <tr>
                                    <td><strong>Language:</strong></td>
                                    <td>{book.language_code}</td>
                                </tr>
                            )}
                            {book.original_publication_year && (
                                <tr>
                                    <td><strong>Publication Year:</strong></td>
                                    <td>{book.original_publication_year}</td>
                                </tr>
                            )}
                        </table>
                    </div>

                    {/* Rate This Book Form */}
                    {isAuthenticated && (
                        <div className="rating-form">
                            <h3>Rate this book</h3>
                            <form onSubmit={handleSubmitRating}>
                                <StarRating rating={userRating} onRatingChange={handleRatingChange} />
                                <textarea
                                    value={userReview}
                                    onChange={handleReviewChange}
                                    placeholder="Write your review (optional)"
                                    rows="4"
                                    className="review-textarea"
                                ></textarea>
                                <button type="submit" className="btn btn-primary">Submit Rating</button>
                            </form>
                        </div>
                    )}
                </div>
            </div>

            {/* Similar Books Section */}
            {similarBooks.length > 0 && (
                <section>
                    <div className="section-heading">
                        <h2 className="section-title">Similar Books</h2>
                        <Link to={`/search?similar=${bookId}`} className="section-link">View more</Link>
                    </div>
                    <div className="books-grid">
                        {similarBooks.slice(0, 4).map((book) => (
                            <BookCard key={book.book_id} book={book} />
                        ))}
                    </div>
                </section>
            )}

            {/* Reviews Section */}
            {reviews.length > 0 && (
                <section>
                    <div className="section-heading">
                        <h2 className="section-title">Reviews</h2>
                    </div>
                    <div className="reviews-list">
                        {reviews.slice(0, 5).map((review, index) => (
                            <div key={index} className="review-item">
                                <div className="review-header">
                                    <span className="review-user">{review.username}</span>
                                    <span className="review-rating">
                                        {Array.from({ length: 5 }, (_, i) => (
                                            <span key={i} className={i < review.rating ? "star full" : "star empty"}>
                                                {i < review.rating ? "★" : "☆"}
                                            </span>
                                        ))}
                                    </span>
                                    <span className="review-date">
                                        {new Date(review.timestamp).toLocaleDateString()}
                                    </span>
                                </div>
                                <p className="review-text">{review.review}</p>
                            </div>
                        ))}
                    </div>
                </section>
            )}
        </div>
    );
};

export default BookDetailsPage;