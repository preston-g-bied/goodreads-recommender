// frontend/goodbooks-client/src/services/recommendationService.js

import api from './api'

/**
 * Get popular book recommendations
 * @param {number} limit - Number of recommendations to return
 * @param {boolean} excludeRated - Whether to exclude books the user has already rated
 * @returns {Promise} - Response from the API
 */
export const getPopularRecommendations = async (limit = 10, excludeRated = false) => {
    try {
        const response = await api.get('/recommendations/popular', {
            params: {
                limit,
                exclude_rated: excludeRated
            }
        });
        return response.data;
    } catch (error) {
        console.error('Error fetching popular recommendations:', error);
        throw error;
    }
};

/**
 * Get personalized recommendations for the current user
 * @param {number} limit - Number of recommendations to return
 * @returns {Promise} - Response from the API
 */
export const getPersonalizedRecommendations = async (limit = 10) => {
    try {
        const response = await api.get('/recommendations/personalized', {
            params: { limit }
        });
        return response.data;
    } catch (error) {
        console.error('Error fetching personalized recommendations:', error);
        throw error;
    }
};