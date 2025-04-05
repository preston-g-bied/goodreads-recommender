// frontend/goodbooks-client/src/components/common/BookCard.js

import React from 'react';
import { Link } from 'react-router-dom';
import './BookCard.css';

const BookCard = ({ book }) => {
    const {
        book_id,
        title,
        authors,
        average_rating,
        image_url,
        publication_year
    } = book;

    // format rating to display stars
    const renderStars = (rating) => {
        const fullStars = Math.floor(rating);
        const hasHalfStar = rating % 1 >= 0.5;
        const stars = [];

        // add full stars
        for (let i = 0; i < fullStars; i++) {
            stars.push(<span key={`full-${i}`} className="star full">★</span>);
        }

        // add half star if needed
        if (hasHalfStar) {
            stars.push(<span key="half" className="star half">★</span>);
        }

        // add empty stars
        const emptyStars = 5 - stars.length;
        for (let i = 0; i < emptyStars; i++) {
            stars.push(<span key={`empty-${i}`} className="star empty">☆</span>);
        }

        return (
            <div className="book-rating">
                <span className="stars">{stars}</span>
                <span className="rating-value">{rating.toFixed(1)}</span>
            </div>
        );
    };

    return (
        <div className="book-card">
            <Link to={`/books/${book_id}`} className="book-card-link">
                <div className="book-cover">
                    {image_url ? (
                        <img src={image_url} alt={`Cover of ${title}`} />
                    ) : (
                        <div className="book-cover-placeholder">
                            No Cover
                        </div>
                    )}
                </div>
                <div className="book-info">
                    <h3 className="book-title">{title}</h3>
                    <p className="book-author">{authors}</p>
                    {average_rating && renderStars(average_rating)}
                    {publication_year && (
                        <p className="book-year">{publication_year}</p>
                    )}
                </div>
            </Link>
        </div>
    );
};

export default BookCard;