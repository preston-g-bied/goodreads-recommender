// frontend/goodbooks-client/src/services/userService.js

import api from './api'

/**
 * Get current user's profile
 * @returns {Promise} - Response from the API
 */
export const getUserProfile = async () => {
    try {
        const response = await api.get('/users/profile');
        return response.data;
    } catch (error) {
        console.error('Error fetching user profile:', error);
        throw error;
    }
};

/**
 * Update user profile
 * @param {Object} profileData - Profile data to update
 * @returns {Promise} - Response from the API
 */
export const updateUserProfile = async (profileData) => {
    try {
        const response = await api.put('/users/profile', profileData);
        return response.data;
    } catch (error) {
        console.error('Error updating user profile:', error);
        throw error;
    }
};

/**
 * Get user's ratings
 * @param {Object} params - Query parameters
 * @returns {Promise} - Response from the API
 */
export const getUserRatings = async (params = {}) => {
    try {
        const response = await api.get('/users/ratings', { params });
        return response.data;
    } catch (error) {
        console.error('Error fetching user ratings:', error);
        throw error;
    }
};

/**
 * Get user's to-read list
 * @param {Object} params - Query parameters
 * @returns {Promise} - Response from the API
 */
export const getToReadList = async (params = {}) => {
    try {
        const response = await api.get('/users/to-read', { params });
        return response.data;
    } catch (error) {
        console.error('Error fetching to-read list:', error);
        throw error;
    }
};

/**
 * Add a book to the to-read list
 * @param {number} bookId - Book ID
 * @returns {Promise} - Response from the API
 */
export const addToReadingList = async (bookId) => {
    try {
        const response = await api.post(`/users/to-read/${bookId}`);
        return response.data;
    } catch (error) {
        console.error(`Error adding book ${bookId} to reading list:`, error);
        throw error;
    }
};

/**
 * Remove a book from the to-read list
 * @param {number} bookId - Book ID
 * @returns {Promise} - Response from the API
 */
export const removeFromReadingList = async (bookId) => {
    try {
        const response = await api.delete(`/users/to-read/${bookId}`);
        return response.data;
    } catch (error) {
        console.error(`Error removing ${bookId} from reading list:`, error);
        throw error;
    }
};

/**
 * Get user activity
 * @param {Object} params - Query parameters
 * @returns {Promise} - Response from the API
 */
export const getUserActivity = async (params = {}) => {
    try {
        const response = await api.get('/users/activity', { params });
        return response.data;
    } catch (error) {
        console.error('Error fetching user activity:', error);
        throw error;
    }
};

/**
 * Get user statistics
 * @returns {Promise} - Response from the API
 */
export const getUserStats = async () => {
    try {
        const response = await api.get('/users/stats');
        return response.data;
    } catch (error) {
        console.error('Error fetching user stats:', error);
        throw error;
    }
};