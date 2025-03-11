import React from 'react';
import { Link } from 'react-router-dom';
import './Home.css';

const Home = () => {
  return (
    <div className="home-container">
      <div className="hero-content">
        <h1>Cinémas Toulouse</h1>
        <p>Trouvez toutes les séances de cinéma à Toulouse en un seul endroit</p>
        <Link to="/seances" className="cta-button">
          Voir les séances
          <span className="arrow">→</span>
        </Link>
      </div>
    </div>
  );
};

export default Home; 