// frontend/goodbooks-client/src/App.js

import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'

// import page components
import HomePage from './components/home/HomePage';
import BookDetailsPage from './components/books/BookDetailsPage';
import SearchResultsPage from './components/search/SearchResultsPage';
import LoginPage from './components/user/LoginPage';
import RegisterPage from './components/user/RegisterPage';
import ProfilePage from './components/user/ProfilePage';
import ReadingListPage from './components/user/ReadingListPage';
import NotFoundPage from './components/common/NotFoundPage';

// import common components
import Header from './components/common/Header';
import Footer from './components/common/Footer';
import ProtectedRoute from './components/common/ProtectedRoute';

// import CSS
import './assets/css/Ap.css';

function App() {
    return (
        <AuthProvider>
            <Router>
                <div className="app">
                    <Header />
                    <main className="main-content">
                        <Routes>
                            {/* Public routes */}
                            <Route path="/" element={<HomePage />} />
                            <Route path="/books/:bookId" element={<BookDetailsPage />} />
                            <Route path="/search" element={<SearchResultsPage />} />
                            <Route path="/login" element={<LoginPage />} />
                            <Route path="/register" element={<RegisterPage />} />

                            {/* Protected routes */}
                            <Route
                                path="/profile"
                                element={
                                    <ProtectedRoute>
                                        <ProfilePage />
                                    </ProtectedRoute>
                                }
                            />
                            <Route
                                path="/reading-list"
                                element={
                                    <ProtectedRoute>
                                        <ReadingListPage />
                                    </ProtectedRoute>
                                }
                            />

                            {/* 404 Route */}
                            <Route path="*" element={<NotFoundPage />} />
                        </Routes>
                    </main>
                    <Footer />
                </div>
            </Router>
        </AuthProvider>
    );
}

export default App;