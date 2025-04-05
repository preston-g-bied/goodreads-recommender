// frontend/goodbooks-client/src/context/AuthContext.js

import React, { createContext, useState, useEffect } from 'react';
import api from '../services/api'

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [currentUser, setCurrentUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        // check if user is logged on in component mount
        const checkUserStatus = async () => {
            const token = localStorage.getItem('token');

            if (!token) {
                setLoading(false);
                return;
            }

            try {
                const response = await api.get('/auth/me');
                if (response.data.success) {
                    setCurrentUser(response.data.data);
                }
            } catch (err) {
                console.error('Error checking authentication status:', err);
                localStorage.removeItem('token');
            } finally {
                setLoading(false);
            }
        };

        checkUserStatus();
    }, []);

    const login = async (username, password) => {
        try {
            setError(null);
            const response = await api.post('/auth/login', { username, password });

            if (response.data.success) {
                localStorage.setItem('token', response.data.data.token);
                setCurrentUser(response.data.data);
                return true;
            }
        } catch (err) {
            setError(err.response?.data?.message || 'Login failed');
            return false;
        }
    };

    const register = async (userData) => {
        try {
            setError(null);
            const response = await api.post('/auth/register', userData);

            if (response.data.success) {
                localStorage.setItem('token', response.data.data.token);
                setCurrentUser(response.data.data);
                return true;
            }
        } catch (err) {
            setError(err.response?.data?.message || 'Registration failed');
            return false
        }
    };

    const logout = () => {
        localStorage.removeItem('token');
        setCurrentUser(null);
    };

    return (
        <AuthContext.Provider
            value={{
                currentUser,
                loading,
                error,
                login,
                register,
                logout,
                isAuthenticated: !!currentUser
            }}
        >
            {children}
        </AuthContext.Provider>
    );
};

// custom hook for using auth context
export const useAuth = () => {
    const context = React.useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider')
    }
    return context;
};