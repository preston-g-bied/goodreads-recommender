// frontend/goodbooks-client/src/components/search/SearchResultsPage.js

import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { searchBooks, getBooks, getTags } from '../../services/bookService';
import BookCard from '../common/BookCard';
import SearchFilters from './SearchFilters';
import Pagination from '../common/Pagination';
import './SearchResultsPage.css';

const SearchResultsPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [books, setBooks] = useState([]);
  const [tags, setTags] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [pagination, setPagination] = useState({
    total: 0,
    pages: 0,
    current_page: 1,
    per_page: 20
  });
  
  // Get query parameters from URL
  const queryParams = new URLSearchParams(location.search);
  const searchQuery = queryParams.get('q') || '';
  const page = parseInt(queryParams.get('page')) || 1;
  const sortBy = queryParams.get('sort_by') || 'relevance';
  const minRating = parseFloat(queryParams.get('min_rating')) || 0;
  const tagName = queryParams.get('tag_name') || '';
  const tagId = parseInt(queryParams.get('tag_id')) || 0;
  const author = queryParams.get('author') || '';
  const yearFrom = parseInt(queryParams.get('year_from')) || 0;
  const yearTo = parseInt(queryParams.get('year_to')) || 0;
  const view = queryParams.get('view') || 'grid';
  
  // Fetch books based on query parameters
  useEffect(() => {
    const fetchBookData = async () => {
      try {
        setLoading(true);
        setError(null);
        
        let response;
        
        // Search based on query or get books with filters
        if (searchQuery) {
          response = await searchBooks(searchQuery, {
            page,
            per_page: pagination.per_page,
            sort_by: sortBy,
            min_rating: minRating,
            tag_id: tagId,
            tag_name: tagName,
            author,
            year_from: yearFrom,
            year_to: yearTo
          });
        } else {
          response = await getBooks({
            page,
            per_page: pagination.per_page,
            sort_by: sortBy,
            min_rating: minRating,
            tag_id: tagId,
            tag_name: tagName,
            author,
            year_from: yearFrom,
            year_to: yearTo
          });
        }
        
        if (response.success) {
          setBooks(response.data.books);
          setPagination(response.data.pagination);
        }
        
        // If viewing tags, fetch tags
        if (view === 'tags') {
          const tagsResponse = await getTags({
            page,
            per_page: 50,
            sort_by: 'popularity'
          });
          
          if (tagsResponse.success) {
            setTags(tagsResponse.data.tags);
          }
        }
      } catch (err) {
        console.error('Error fetching search results:', err);
        setError('Failed to load search results. Please try again later.');
      } finally {
        setLoading(false);
      }
    };
    
    fetchBookData();
  }, [location.search, pagination.per_page]);
  
  // Update URL when filters change
  const updateFilters = (filters) => {
    const newParams = new URLSearchParams();
    
    // Add existing query if present
    if (searchQuery) {
      newParams.set('q', searchQuery);
    }
    
    // Add filters
    if (filters.sort_by) {
      newParams.set('sort_by', filters.sort_by);
    }
    
    if (filters.min_rating > 0) {
      newParams.set('min_rating', filters.min_rating);
    }
    
    if (filters.tag_id) {
      newParams.set('tag_id', filters.tag_id);
    }
    
    if (filters.tag_name) {
      newParams.set('tag_name', filters.tag_name);
    }
    
    if (filters.author) {
      newParams.set('author', filters.author);
    }
    
    if (filters.year_from > 0) {
      newParams.set('year_from', filters.year_from);
    }
    
    if (filters.year_to > 0) {
      newParams.set('year_to', filters.year_to);
    }
    
    if (filters.view && filters.view !== 'grid') {
      newParams.set('view', filters.view);
    }
    
    if (filters.page && filters.page > 1) {
      newParams.set('page', filters.page);
    }
    
    navigate(`/search?${newParams.toString()}`);
  };
  
  // Handle page change
  const handlePageChange = (newPage) => {
    updateFilters({ ...getCurrentFilters(), page: newPage });
  };
  
  // Get current filters from URL
  const getCurrentFilters = () => {
    return {
      sort_by: sortBy,
      min_rating: minRating,
      tag_id: tagId,
      tag_name: tagName,
      author,
      year_from: yearFrom,
      year_to: yearTo,
      view,
      page
    };
  };
  
  // Clear all filters
  const clearFilters = () => {
    const newParams = new URLSearchParams();
    if (searchQuery) {
      newParams.set('q', searchQuery);
    }
    navigate(`/search?${newParams.toString()}`);
  };
  
  if (loading) {
    return <div className="loading">Loading...</div>;
  }
  
  if (error) {
    return <div className="error-message">{error}</div>;
  }
  
  // Render tag view if requested
  if (view === 'tags') {
    return (
      <div className="search-page">
        <h1>Browse By Tags</h1>
        <div className="tags-grid">
          {tags.map((tag) => (
            <div key={tag.tag_id} className="tag-card">
              <h3 className="tag-name">
                <a href={`/search?tag_id=${tag.tag_id}`}>{tag.tag_name}</a>
              </h3>
              <div className="tag-count">{tag.book_count} books</div>
            </div>
          ))}
        </div>
        <Pagination
          currentPage={pagination.current_page}
          totalPages={pagination.pages}
          onPageChange={handlePageChange}
        />
      </div>
    );
  }
  
  return (
    <div className="search-page">
      {/* Search Filters */}
      <SearchFilters
        currentFilters={getCurrentFilters()}
        onFilterChange={updateFilters}
        onClearFilters={clearFilters}
      />
      
      {/* Search Results Counter */}
      <div className="search-results-count">
        {books.length > 0 ? (
          <p>
            Showing {(pagination.current_page - 1) * pagination.per_page + 1}-
            {Math.min(pagination.current_page * pagination.per_page, pagination.total)} of {pagination.total} results
            {searchQuery ? ` for "${searchQuery}"` : ''}
          </p>
        ) : (
          <p>No results found{searchQuery ? ` for "${searchQuery}"` : ''}</p>
        )}
      </div>
      
      {/* Search Results Grid */}
      {books.length > 0 ? (
        <div className={`books-${view === 'list' ? 'list' : 'grid'}`}>
          {books.map((book) => (
            <BookCard key={book.book_id} book={book} />
          ))}
        </div>
      ) : (
        <div className="no-results">
          <p>No books found matching your criteria.</p>
          <button onClick={clearFilters} className="btn btn-primary">
            Clear Filters
          </button>
        </div>
      )}
      
      {/* Pagination */}
      {pagination.pages > 1 && (
        <Pagination
          currentPage={pagination.current_page}
          totalPages={pagination.pages}
          onPageChange={handlePageChange}
        />
      )}
    </div>
  );
};

export default SearchResultsPage;