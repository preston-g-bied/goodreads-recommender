// frontend/goodbooks-client/src/components/common/ProtectedRoute.js

import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

const ProtectedRoute = ({ children }) => {
    const { isAuthenticated, loading } = useAuth();

    // show loading indicator while checking authentications
    if (loading) {
        return <div className="loading">Loading...</div>;
    }

    // redirect to login if not authenticated
    if (!isAuthenticated) {
        return <Navigate to="/login" />;
    }

    // render children if authenticated
    return children;
};

export default ProtectedRoute;