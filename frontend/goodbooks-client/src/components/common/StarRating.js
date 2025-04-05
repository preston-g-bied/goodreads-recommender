// frontend/goodbooks-client/src/components/common/StarRating.js

import React, { useState } from 'react';
import './StarRating.css';

const StarRating = ({ rating = 0, onRatingChange, interactive = true }) => {
    const [hoverRating, setHoverRating] = useState(0);

    const handleMouseEnter = (index) => {
        if (interactive) {
            setHoverRating(index);
        }
    };

    const handleMouseLeave = () => {
        if (interactive) {
            setHoverRating(0);
        }
    };

    const handleClick = (index) => {
        if (interactive && onRatingChange) {
            onRatingChange(index);
        }
    };

    return (
        <div className="star-rating">
            {[1, 2, 3, 4, 5].map((index) => {
                const currentRating = hoverRating || rating;

                return (
                    <span
                        key={index}
                        className={`star ${index <= currentRating ? 'filled' : 'empty'} ${interactive ? 'interactive' : ''}`}
                        onMouseEnter={() => handleMouseEnter(index)}
                        onMouseLeave={handleMouseLeave}
                        onClick={() => handleClick(index)}
                    >
                        {index <= currentRating ? '★' : '☆'}
                    </span>
                );
            })}
        </div>
    );
};

export default StarRating;