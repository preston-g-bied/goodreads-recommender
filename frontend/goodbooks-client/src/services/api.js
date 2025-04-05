// frontend/goodbooks-client/src/services/api.js
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api/v1'

// create axios instance with base URL
const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// request interceptor for adding auth token
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers['Authorization'] =  `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// response interceptor for handling errors
api.interceptors.response.use(
    (response) => {
        return response;
    },
    (error) => {
        // handle authentication errors
        if (error.response && error.response.status === 401) {
            localStorage.removeItem('token');
            // redirect to login if needed
            // window.location.href = '/login';
        }
        return Promise.reject(error)
    }
);

export default api;