// frontend/goodbooks-client/src/components/search/SearchFilters.js

import React, { useState } from 'react';
import './SearchFilters.css';

const SearchFilters = ({ currentFilters, onFilterChange, onClearFilters }) => {
  const [showMobileFilters, setShowMobileFilters] = useState(false);
  
  // Handle filter changes
  const handleFilterChange = (filterName, value) => {
    onFilterChange({
      ...currentFilters,
      [filterName]: value,
      // Reset to page 1 when filters change
      page: 1
    });
  };
  
  // Handle view toggle
  const handleViewToggle = (view) => {
    handleFilterChange('view', view);
  };
  
  // Format filter for display
  const formatFilter = (name, value) => {
    switch (name) {
      case 'min_rating':
        return `${value}+ Stars`;
      case 'tag_name':
        return `Tag: ${value}`;
      case 'author':
        return `Author: ${value}`;
      case 'year_from':
        return `From ${value}`;
      case 'year_to':
        return `To ${value}`;
      default:
        return value;
    }
  };
  
  // Check if filters are active
  const hasActiveFilters = () => {
    return (
      currentFilters.min_rating > 0 ||
      currentFilters.tag_id > 0 ||
      currentFilters.tag_name ||
      currentFilters.author ||
      currentFilters.year_from > 0 ||
      currentFilters.year_to > 0
    );
  };
  
  return (
    <div className="search-filters">
      {/* Toggle Filters Button (Mobile) */}
      <button
        className="filter-toggle-button"
        onClick={() => setShowMobileFilters(!showMobileFilters)}
      >
        {showMobileFilters ? 'Hide Filters' : 'Show Filters'}
      </button>
      
      {/* Filters Container */}
      <div className={`filters-container ${showMobileFilters ? 'show' : ''}`}>
        {/* Rating Filter */}
        <div className="filter-group">
          <label htmlFor="rating-filter">Min Rating:</label>
          <select
            id="rating-filter"
            value={currentFilters.min_rating || 0}
            onChange={(e) => handleFilterChange('min_rating', parseFloat(e.target.value))}
          >
            <option value="0">Any</option>
            <option value="3">3+ Stars</option>
            <option value="4">4+ Stars</option>
            <option value="4.5">4.5+ Stars</option>
          </select>
        </div>
        
        {/* Year Filter */}
        <div className="filter-group">
          <label htmlFor="year-filter">Year:</label>
          <select
            id="year-filter"
            value={currentFilters.year_from || 0}
            onChange={(e) => handleFilterChange('year_from', parseInt(e.target.value))}
          >
            <option value="0">Any</option>
            <option value="2020">2020+</option>
            <option value="2010">2010+</option>
            <option value="2000">2000+</option>
            <option value="1990">1990+</option>
          </select>
        </div>
        
        {/* Sort By Filter */}
        <div className="filter-group">
          <label htmlFor="sort-filter">Sort By:</label>
          <select
            id="sort-filter"
            value={currentFilters.sort_by || 'relevance'}
            onChange={(e) => handleFilterChange('sort_by', e.target.value)}
          >
            <option value="relevance">Relevance</option>
            <option value="rating">Highest Rated</option>
            <option value="popularity">Most Popular</option>
            <option value="year">Newest</option>
            <option value="title">Title</option>
            <option value="author">Author</option>
          </select>
        </div>
      </div>
      
      {/* View Type Toggle */}
      <div className="view-toggle">
        <button
          className={`view-button ${currentFilters.view !== 'list' ? 'active' : ''}`}
          onClick={() => handleViewToggle('grid')}
        >
          Grid View
        </button>
        <button
          className={`view-button ${currentFilters.view === 'list' ? 'active' : ''}`}
          onClick={() => handleViewToggle('list')}
        >
          List View
        </button>
      </div>
      
      {/* Active Filters Display */}
      {hasActiveFilters() && (
        <div className="active-filters">
          <span className="active-filters-label">Active filters:</span>
          <div className="filter-tags">
            {currentFilters.min_rating > 0 && (
              <span className="filter-tag">
                {formatFilter('min_rating', currentFilters.min_rating)}
                <button
                  onClick={() => handleFilterChange('min_rating', 0)}
                  className="remove-filter"
                >
                  ✕
                </button>
              </span>
            )}
            
            {currentFilters.tag_name && (
              <span className="filter-tag">
                {formatFilter('tag_name', currentFilters.tag_name)}
                <button
                  onClick={() => handleFilterChange('tag_name', '')}
                  className="remove-filter"
                >
                  ✕
                </button>
              </span>
            )}
            
            {currentFilters.author && (
              <span className="filter-tag">
                {formatFilter('author', currentFilters.author)}
                <button
                  onClick={() => handleFilterChange('author', '')}
                  className="remove-filter"
                >
                  ✕
                </button>
              </span>
            )}
            
            {currentFilters.year_from > 0 && (
              <span className="filter-tag">
                {formatFilter('year_from', currentFilters.year_from)}
                <button
                  onClick={() => handleFilterChange('year_from', 0)}
                  className="remove-filter"
                >
                  ✕
                </button>
              </span>
            )}
            
            {currentFilters.year_to > 0 && (
              <span className="filter-tag">
                {formatFilter('year_to', currentFilters.year_to)}
                <button
                  onClick={() => handleFilterChange('year_to', 0)}
                  className="remove-filter"
                >
                  ✕
                </button>
              </span>
            )}
            
            <button
              onClick={onClearFilters}
              className="clear-filters"
            >
              Clear All
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default SearchFilters;