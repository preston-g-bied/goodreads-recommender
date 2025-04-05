// frontend/goodbooks-client/src/components/home/HomePage.js

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getPopularBooks } from '../../services/bookService';
import { getTags } from '../../services/bookService';
import { getPopularRecommendations } from '../../services/recommendationService';
import { userAuth } from '../../context/AuthContext';

// import components
import SearchBar from './SearchBar'
import BookCard from '../common/BookCard'
import './HomePage.css'

const HomePage = () => {
    const [popularBooks, setPopularBooks] = useState([]);
    const [topRatedBooks, setTopRatedBooks] = useState([]);
    const [popularTags, setPopularTags] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const { isAuthenticated } = useAuth();
    const navigate = useNavigate();

    useEffect(() => {
        const fetchHomeData = async () => {
            try {
                setLoading(true);
                setError(null);

                // fetch popular books
                const popularResponse = await getPopularBooks(5);
                if (popularResponse.success) {
                    setPopularBooks(popularResponse.data);
                }

                // fetch top-rated books
                const recommendationsResponse = await getPopularRecommendations(5);
                if (recommendationsResponse.success) {
                    setTopRatedBooks(recommendationsResponse.data);
                }

                // fetch popular tags
                const tagsResponse = await getTags({ sort_by: 'popularity', per_page: 12 });
                if (tagsResponse.success) {
                    setPopularTags(tagsResponse.data.tags);
                }
            } catch (err) {
                console.error('Error fetching home page data:', err);
                setError('Failed to load content. Please try again later.');
            } finally {
                setLoading(false);
            }
        };

        fetchHomeData();
    }, []);

    const handleSearch = (query) => {
        navigate(`/search?q=${encodeURIComponent(query)}`);
    };

    if (loading) {
        return <div className="loading">Loading...</div>;
    }

    return (
        <div className="home-page">
            {/* Search Section */}
            <section className="search-container">
                <SearchBar onSearch={handleSearch} />
            </section>

            {error && <div className="error-message">{error}</div>}

            {/* Featured Books Section */}
            <section>
                <div className="section-heading">
                    <h2 className="section-title">Popular Books</h2>
                    <a href="/search?sort=popular" className="section-link">View all</a>
                </div>
                <div className="books-grid">
                    {popularBooks.map((book) => (
                        <BookCard key={book.book_id} book={book} />
                    ))}
                </div>
            </section>

            {/* Top Rated Books Section */}
            <section>
                <div className="section-heading">
                    <h2 className="section-title">Top Rated Books</h2>
                    <a href="/search?sort=rating" className="section-link">View all</a>
                </div>
                <div className="books-grid">
                    {topRatedBooks.map((book) => (
                        <BookCard key={book.book_id} book={book} />
                    ))}
                </div>
            </section>

            {/* Popular Tags Section */}
            <section className="tags-container">
                <div className="section-heading">
                    <h2 className="section-title">Popular Tags</h2>
                    <a href="/search?view=tags" className="section-link">View all tags</a>
                </div>
                <ul className="tags-list">
                    {popularTags.map((tag) => (
                        <li key={tag.tag_id} className="tag-item">
                            <a href={`/search?tag_id=${tag.tag_id}`} className="tag-link">
                                {tag.tag_name}
                            </a>
                        </li>
                    ))}
                </ul>
            </section>
        </div>
    );
};

export default HomePage;