// frontend/goodbooks-client/src/components/user/LoginPage.js

import React, { useState, useEffect } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import './LoginPage.css';

const LoginPage = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [rememberMe, setRememberMe] = useState(false);
    const [error, setError] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);

    const { login, isAuthenticated, error: authError } = useAuth();
    const navigate = useNavigate();
    const location = useLocation();

    // get the redirect path from location state or default to home
    const from = location.state?.from?.pathname || '/';

    // redirect if already authenticated
    useEffect(() => {
        if (isAuthenticated) {
            navigate(from, { replace: true });
        }
    }, [isAuthenticated, navigate, from]);

    // update error message if auth context has error
    useEffect(() => {
        if (authError) {
            setError(authError);
        }
    }, [authError]);

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!username || !password) {
            setError('Please enter both username and password');
            return;
        }

        try {
            setError('');
            setIsSubmitting(true);

            const success = await login(username, password);

            if (success) {
                // login successful, will redirect via useEffect
            }
        } catch (err) {
            setError('An unexpected error occured. Please try again.')
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <div className="container">
            <div className="form-container">
                <h1 className="form-title">Login to Goodbooks</h1>

                {error && <div classname="error-message">{error}</div>}

                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label htmlFor="username" className="form-label">Username</label>
                        <input
                            type="text"
                            id="username"
                            className="form-input"
                            placeholder="Enter your username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="password" className="form-label">Password</label>
                        <input
                            type="password"
                            id="password"
                            className="form-input"
                            placeholder="Enter your password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </div>

                    <div className="form-options">
                        <div className="remember-me">
                            <input
                                type="checkbox"
                                id="remember-me"
                                checked={rememberMe}
                                onChange={(e) => setRememberMe(e.target.checked)}
                            />
                            <label htmlFor="remember-me">Remember me</label>
                        </div>

                        <div className="forgot-password">
                            <Link to="/forgot-password">Forgot password?</Link>
                        </div>
                    </div>

                    <button
                        type="submit"
                        className="form-button"
                        disabled={isSubmitting}
                    >
                        {isSubmitting ? 'Logging in...' : 'Login'}
                    </button>
                </form>

                <div className="form-footer">
                    <p>Don't have an account? <Link to="/register">Register</Link></p>
                </div>
            </div>
        </div>
    );
};

export default LoginPage;