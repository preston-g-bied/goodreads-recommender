// frontend/goodbooks-client/src/components/common/Header.js

import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import './Header.css';

const Header = () => {
    const { currentUser, isAuthenticated, logout } = useAuth();
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate('/');
    };

    return (
        <header className="header">
            <div className="container header-container">
                <div className="logo">
                    <Link to="/">Goodbooks</Link>
                </div>
                <nav>
                    <ul className="nav-links">
                        <li><Link to="/">Home</Link></li>
                        <li><Link to="/search">Browse</Link></li>

                        {isAuthenticated ? (
                            <>
                                <li><Link to="/profile">Profile</Link></li>
                                <li><Link to="/reading-list">Reading List</Link></li>
                                <li>
                                    <button onClick={handleLogout} className="logout-button">
                                        Logout
                                    </button>
                                </li>
                            </>
                        ) : (
                            <>
                                <li><Link to="/login">Login</Link></li>
                                <li><Link to="/register">Register</Link></li>
                            </>
                        )}
                    </ul>
                </nav>
            </div>
        </header>
    );
};

export default Header;