// frontend/goodbooks-client/src/components/common/Footer.js

import React from 'react';
import { Link } from 'react-router-dom';

const Footer = () => {
  const currentYear = new Date().getFullYear();
  
  return (
    <footer className="footer">
      <div className="container footer-container">
        <div className="footer-section">
          <h3>About Goodbooks</h3>
          <ul className="footer-links">
            <li><Link to="#">About Us</Link></li>
            <li><Link to="#">Our Team</Link></li>
            <li><Link to="#">Terms of Service</Link></li>
            <li><Link to="#">Privacy Policy</Link></li>
          </ul>
        </div>
        <div className="footer-section">
          <h3>Discover</h3>
          <ul className="footer-links">
            <li><Link to="/search">Browse Books</Link></li>
            <li><Link to="/search?view=tags">Tags</Link></li>
            <li><Link to="/search?sort=popular">Popular Books</Link></li>
            <li><Link to="/search?sort=recent">New Releases</Link></li>
          </ul>
        </div>
        <div className="footer-section">
          <h3>Community</h3>
          <ul className="footer-links">
            <li><Link to="#">Reading Challenges</Link></li>
            <li><Link to="#">Discussion Forums</Link></li>
            <li><Link to="#">Book Clubs</Link></li>
            <li><Link to="#">Help Center</Link></li>
          </ul>
        </div>
      </div>
      <div className="copyright">
        <p>© {currentYear} Goodbooks. All rights reserved.</p>
      </div>
    </footer>
  );
};

export default Footer;