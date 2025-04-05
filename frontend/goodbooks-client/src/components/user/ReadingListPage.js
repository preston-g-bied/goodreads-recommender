// frontend/goodbooks-client/src/components/user/ReadingListPage.js

import React, { useState, useEffect } from 'react';
import { getToReadList, removeFromReadingList } from '../../services/userService';
import BookCard from '../common/BookCard';
import './ProfilePage.css'; // Reuse ProfilePage styles

const ReadingListPage = () => {
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState('');
  
  useEffect(() => {
    const fetchReadingList = async () => {
      try {
        setLoading(true);
        setError(null);
        
        const response = await getToReadList();
        if (response.success) {
          setBooks(response.data.to_read);
        }
      } catch (err) {
        console.error('Error fetching reading list:', err);
        setError('Failed to load reading list. Please try again later.');
      } finally {
        setLoading(false);
      }
    };
    
    fetchReadingList();
  }, []);
  
  const handleRemoveBook = async (bookId) => {
    try {
      const response = await removeFromReadingList(bookId);
      if (response.success) {
        setBooks(books.filter(book => book.book_id !== bookId));
        setSuccessMessage('Book removed from reading list');
        setTimeout(() => setSuccessMessage(''), 3000);
      }
    } catch (err) {
      setError('Failed to remove book. Please try again.');
      setTimeout(() => setError(''), 3000);
    }
  };
  
  if (loading) {
    return <div className="loading">Loading...</div>;
  }
  
  return (
    <div className="reading-list-page">
      <h1>My Reading List</h1>
      
      {successMessage && <div className="success-message">{successMessage}</div>}
      {error && <div className="error-message">{error}</div>}
      
      {books.length > 0 ? (
        <div className="books-grid">
          {books.map((book) => (
            <div key={book.book_id} className="reading-list-item">
              <BookCard book={book} />
              <button 
                className="remove-button"
                onClick={() => handleRemoveBook(book.book_id)}
              >
                Remove from list
              </button>
            </div>
          ))}
        </div>
      ) : (
        <div className="empty-state">
          <p>Your reading list is empty. Browse books and add them to your reading list!</p>
        </div>
      )}
    </div>
  );
};

export default ReadingListPage;