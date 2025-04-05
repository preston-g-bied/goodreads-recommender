// frontend/goodbooks-client/src/components/user/ProfilePage.js

import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getUserProfile, getUserRatings, getUserStats } from '../../services/userService';
import { getPersonalizedRecommendations } from '../../services/recommendationService';
import { useAuth } from '../../context/AuthContext';
import BookCard from '../common/BookCard';
import './ProfilePage.css';

const ProfilePage = () => {
    const { currentUser } = useAuth();
    const [profile, setProfile] = useState(null);
    const [userRatings, setUserRatings] = useState([]);
    const [recommendations, setRecommendations] = useState([]);
    const [userStats, setUserStats] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [activeTab, setActiveTab] = useState('ratings');

    useEffect(() => {
        const fetchProfileData = async () => {
            try {
                setLoading(true);
                setError(null);

                // fetch user profile data
                const profileResponse = await getUserProfile();
                if (profileResponse.success) {
                    setProfile(profileResponse.data);
                }

                // fetch user ratings
                const ratingsResponse = await getUserRatings({ per_page: 4 });
                if (ratingsResponse.success) {
                    setUserRatings(ratingsResponse.data.ratings);
                }

                // fetch personalized recommendations
                const recommendationsResponse = await getPersonalizedRecommendations(4);
                if (recommendationsResponse.success) {
                    setRecommendations(recommendationsResponse.data)
                }

                // fetch user stats
                const statsResponse = await getUserStats();
                if (statsResponse.success) {
                    setUserStats(statsResponse.data)
                }
            } catch (err) {
                console.error('Error fetching profile data:', err);
                setError('Failed to load profile data. Please try again later.')
            } finally {
                setLoading(false);
            }
        };

        fetchProfileData();
    }, []);

    if (loading) {
        return <div className="loading">Loading...</div>;
    }

    if (error) {
        return <div className="error-message">{error}</div>;
    }

    if (!profile || !currentUser) {
        return <div className="error-message">Failed to load profile</div>;
    }

    return (
        <div className="profile-page">
            {/* Profile Header */}
            <div className="profile-header">
                <div className="profile-image">
                    {profile.profile_image ? (
                        <img src={profile.profile_image} alt={`${currentUser.username}'s profile`} />
                    ) : (
                        <div className="profile-image-placeholder">{currentUser.username.charAt(0).toUpperCase()}</div>
                    )}
                </div>
                <div className="profile-info">
                    <h1>{currentUser.username}</h1>
                    <p>Member since {new Date(profile.joined_date).toLocaleDateString()}</p>
                </div>
            </div>

            {/* Profile Stats */}
            {userStats && (
                <div className="profile-stats">
                    <div className="stat-item">
                        <div className="stat-value">{userStats.ratings.count}</div>
                        <div className="stat-label">Books Read</div>
                    </div>
                    <div className="stat-item">
                        <div className="stat-value">{profile.stats.to_read_count}</div>
                        <div className="stat-label">To Read</div>
                    </div>
                    <div className="stat-item">
                        <div className="stat-value">{userStats.ratings.average.toFixed(1)}</div>
                        <div className="stat-label">Avg Rating</div>
                    </div>
                </div>
            )}

            {/* Tab Navigation */}
            <div className="profile-tabs">
                <button
                    className={`tab-button ${activeTab === 'ratings' ? 'active' : ''}`}
                    onClick={() => setActiveTab('ratings')}
                >
                    My Ratings
                </button>
                <button
                    className={`tab-button ${activeTab === 'to-read' ? 'active' : ''}`}
                    onClick={() => setActiveTab('to-read')}
                >
                    Reading List
                </button>
                <button
                    className={`tab-button ${activeTab === 'recommendations' ? 'active' : ''}`}
                    onClick={() => setActiveTab('recommendations')}
                >
                    Recommendations
                </button>
                {userStats && userStats.most_read_tags.length > 0 && (
                    <button
                        className={`tab-button ${activeTab === 'stats' ? 'active' : ''}`}
                        onClick={() => setActiveTab('stats')}
                    >
                        Stats
                    </button>
                )}
            </div>

            {/* Tab Content */}
            <div className="tab-content">
                {activeTab === 'ratings' && (
                    <div className="ratings-tab">
                        <div className="section-heading">
                            <h2 className="section-title">My Ratings</h2>
                            <Link to="/ratings" className="section-link">View all</Link>
                        </div>
                        {userRatings.length > 0 ? (
                            <div className="books-grid">
                                {userRatings.map((rating) => (
                                    <div key={rating.book_id} className="book-rating-card">
                                        <BookCard book={{
                                            book_id: rating.book_id,
                                            title: rating.title,
                                            authors: rating.authors,
                                            image_url: rating.image_url
                                        }} />
                                        <div className="user-rating">
                                            Your rating:
                                            <span className="rating-stars">
                                                {Array.from({ length: 5 }, (_, i) => (
                                                    <span key={i} className={i < rating.rating ? "star full" : "star empty"}>
                                                        {i < rating.rating ? "★" : "☆"}
                                                    </span>
                                                ))}
                                            </span>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        ) : (
                            <p className="empty-state">You haven't rated any books yet.</p>
                        )}
                    </div>
                )}

                {activeTab === 'to-read' && (
                    <div className="to-read-tab">
                        <div className="section-heading">
                            <h2 className="section-title">My Reading List</h2>
                            <Link to="/reading-list" className="section-link">View all</Link>
                        </div>
                        {profile.stats.to_read_count > 0 ? (
                            <p className="redirect-message">
                                View your full reading list <Link to="/reading-list">here</Link>.
                            </p>
                        ) : (
                            <p className="empty-state">Your reading list is empty.</p>
                        )}
                    </div>
                )}

                {activeTab === 'recommendations' && (
                    <div className="recommendations-tab">
                        <div className="section-heading">
                            <h2 className="section-title">Recommended For You</h2>
                            <button className="section-link">Refresh</button>
                        </div>
                        {recommendations.length > 0 ? (
                            <div className="books-grid">
                                {recommendations.map((book) => (
                                    <BookCard key={book.book_id} book={book} />
                                ))}
                            </div>
                        ) : (
                            <p className="empty-state">
                                Rate more books to get personalized recommendations.
                            </p>
                        )}
                    </div>
                )}

                {activeTab === 'stats' && userStats && (
                    <div className="stats-time">
                        <div className="section-heading">
                            <h2 className="section-title">Reading Stats</h2>
                        </div>

                        <div className="stats-grid">
                            <div className="stats-card">
                                <h3>Ratings Distribution</h3>
                                <div className="rating-distribution">
                                    {[5, 4, 3, 2, 1].map((star) => {
                                        const count = userStats.ratings.distribution[`${star}_star`] || 0;
                                        const total = userStats.ratings.count || 1;
                                        const percentage = Math.round((count / total) * 100);

                                        return (
                                            <div key={star} className="rating-bar">
                                                <span className="rating-label">{star} ★</span>
                                                <div className="rating-bar-container">
                                                    <div
                                                        className="rating-bar-fill"
                                                        style={{ width: `${percentage}%` }}
                                                    ></div>
                                                </div>
                                                <span className="rating-count">{count}</span>
                                            </div>
                                        );
                                    })}
                                </div>
                            </div>

                            <div className="stats-card">
                                <h3>Favorite Authors</h3>
                                {userStats.most_read_authors.length > 0 ? (
                                    <ul className="stats-list">
                                        {userStats.most_read_authors.map((item, index) => (
                                            <li key={index} className="stats-list-item">
                                                <span className="stats-item-name">{item.author}</span>
                                                <span className="stats-item-count">{item.count}</span>
                                            </li>
                                        ))}
                                    </ul>
                                ) : (
                                    <p className="empty-state">No author data available</p>
                                )}
                            </div>

                            <div className="stats-card">
                                <h3>Favorite Genres</h3>
                                {userStats.most_read_tags.length > 0 ? (
                                    <ul className="stats-list">
                                        {userStats.most_read_tags.map((item, index) => (
                                            <li key={index} className="stats-list-item">
                                                <span className="stats-item-name">{item.tag}</span>
                                                <span className="stats-item-count">{item.count}</span>
                                            </li>
                                        ))}
                                    </ul>
                                ) : (
                                    <p className="empty-state">No genre data available</p>
                                )}
                            </div>
                        </div>
                    </div>
                )}
            </div>

            {/* Account Settings Button */}
            <div className="profile-actions">
                <Link to="/profile/edit" className="btn btn-secondary">Edit Profile Settings</Link>
            </div>
        </div>
    );
};

export default ProfilePage;