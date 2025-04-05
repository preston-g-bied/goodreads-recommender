// frontend/goodbooks-client/src/services/bookService.js

import api from './api'

/**
 * Get books with optional filtering
 * @param {Object} params - Query parameters
 * @returns {Promise} - Response from the API
 */
export const getBooks = async (params = {}) => {
    try {
        const response = await api.get('/books/', { params });
        return response.data;
    } catch (error) {
        console.error('Error fetching books:', error);
        throw error;
    }
};

/**
 * Get a specific book by ID
 * @param {number} bookId - Book ID
 * @returns {Promise} - Response from the API
 */
export const getBookById = async (bookId) => {
    try {
        const response = await api.get(`books/${bookId}`);
        return response.data;
    } catch (error) {
        console.error(`Error fetching book ${bookId}:`, error);
        throw error;
    }
};

/**
 * Search books by query string
 * @param {string} query - Search query
 * @param {Object} params - Additional parameters
 * @returns {Promise} - Response from the API
 */
export const searchBooks = async (query, params = {}) => {
    try {
        const response = await api.get('/books/search', {
            params: {
                q: query,
                ...params
            }
        });
        return response.data;
    } catch (error) {
        console.error('Error searching books:', error);
        throw error;
    }
};

/**
 * Get popular books
 * @param {number} limit - Number of books to return
 * @returns {Promise} - Response from the API
 */
export const getPopularBooks = async (limit = 10) => {
    try {
        const response = await api.get('/books/popular', {
            params: { limit }
        });
        return response.data;
    } catch (error) {
        console.error('Error fetching popular books:', error);
        throw error
    }
};

/**
 * Get book tags
 * @param {Object} params - Query parameters
 * @returns {Promise} - Response from the API
 */
export const getTags = async (params = {}) => {
    try {
        const response = await api.get('/books/tags', { params });
        return response.data;
    } catch (error) {
        console.error('Error fetching tags:', error);
        throw error;
    }
};

/**
 * Rate a book
 * @param {number} bookId - Book ID
 * @param {number} rating - Rating value (1-5)
 * @param {string} review - Optional review text
 * @returns {Promise} - Response from the API
 */
export const rateBook = async (bookId, rating, review = '') => {
    try {
        const response = await api.put(`/books/rate/${bookId}`, { rating, review });
        return response.data;
    } catch (error) {
        console.error(`Error rating book ${bookId}:`, error);
        throw error;
    }
};

/**
 * Get book reviews
 * @param {number} bookId - Book ID
 * @param {Object} params - Query parameters
 * @returns {Promise} - Response from the API
 */
export const getBookReviews = async (bookId, params = {}) => {
    try {
        const response = await api.get(`/books/reviews/${bookId}`, { params });
        return response.data;
    } catch (error) {
        console.error(`Error fetching reviews for book ${bookId}:`, error);
        throw error;
    }
};

/**
 * Get similar books
 * @param {number} bookId - Book ID
 * @returns {Promise} - Response from the API
 */
export const getSimilarBooks = async (bookId) => {
    try {
        const response = await api.get(`/books/similar/${bookId}`);
        return response.data;
    } catch (error) {
        console.error(`Error fetching similar books for ${bookId}:`, error);
        throw error;
    }
};