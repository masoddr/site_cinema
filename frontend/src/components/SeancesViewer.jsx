import React, { useState, useEffect } from 'react';
import FilmModal from './FilmModal';
import './SeancesViewer.css';

const SeancesViewer = ({ seances }) => {
  const [selectedDate, setSelectedDate] = useState(
    seances.length > 0 ? seances[0].jour.split('T')[0] : null
  );
  const [selectedFilm, setSelectedFilm] = useState(null);
  const [selectedCinemas, setSelectedCinemas] = useState(new Set());
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [showFilters, setShowFilters] = useState(false);
  const filterRef = React.useRef(null); // Référence pour le menu de filtrage

  const cinemas = [...new Set(seances.map(s => s.cinema))];

  React.useEffect(() => {
    setSelectedCinemas(new Set(cinemas));
  }, []);

  // Initialiser le mode sombre depuis localStorage uniquement côté client
  useEffect(() => {
    const savedMode = localStorage.getItem('darkMode');
    if (savedMode !== null) {
      setIsDarkMode(JSON.parse(savedMode));
    }
  }, []);

  // Sauvegarder la préférence de thème
  useEffect(() => {
    if (typeof window !== 'undefined') { // Vérifier qu'on est côté client
      localStorage.setItem('darkMode', JSON.stringify(isDarkMode));
      document.body.classList.toggle('dark-mode', isDarkMode);
    }
  }, [isDarkMode]);

  // Gestionnaire pour fermer le menu lors d'un clic à l'extérieur
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (filterRef.current && !filterRef.current.contains(event.target)) {
        setShowFilters(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  const seancesByFilm = seances.reduce((acc, seance) => {
    if (seance.jour.split('T')[0] === selectedDate && selectedCinemas.has(seance.cinema)) {
      if (!acc[seance.titre]) {
        acc[seance.titre] = {
          titre: seance.titre,
          duree: seance.duree,
          seances: []
        };
      }
      acc[seance.titre].seances.push(seance);
    }
    return acc;
  }, {});

  const dates = [...new Set(seances.map(s => s.jour.split('T')[0]))];

  const handleCinemaToggle = (cinema) => {
    const newSelectedCinemas = new Set(selectedCinemas);
    if (newSelectedCinemas.has(cinema)) {
      newSelectedCinemas.delete(cinema);
    } else {
      newSelectedCinemas.add(cinema);
    }
    setSelectedCinemas(newSelectedCinemas);
  };

  return (
    <div className={`seances-viewer ${isDarkMode ? 'dark-mode' : ''}`}>
      <nav className="top-navbar">
        <div className="nav-left">
          <a href="/" className="home-link">
            <span className="arrow-back">←</span>
            <span className="home-text">Accueil</span>
          </a>
        </div>
        <div className="nav-center">
          <div className="cinema-filters" ref={filterRef}>
            <button 
              className="filter-toggle"
              onClick={() => setShowFilters(!showFilters)}
            >
              Cinémas <span className="filter-count">({selectedCinemas.size})</span>
            </button>
            <div className={`filter-dropdown ${showFilters ? 'show' : ''}`}>
              {cinemas.map(cinema => (
                <label key={cinema} className="cinema-checkbox">
                  <input
                    type="checkbox"
                    checked={selectedCinemas.has(cinema)}
                    onChange={() => handleCinemaToggle(cinema)}
                  />
                  {cinema}
                </label>
              ))}
            </div>
          </div>
        </div>
        <div className="nav-right">
          <div className="theme-toggle">
            <label className="switch">
              <input
                type="checkbox"
                checked={isDarkMode}
                onChange={() => setIsDarkMode(!isDarkMode)}
              />
              <span className="slider">
                <span className="sun">☀️</span>
                <span className="moon">🌙</span>
              </span>
            </label>
          </div>
        </div>
      </nav>

      <main className="main-content">
        <div className="date-selector">
          {dates.map(date => (
            <button
              key={date}
              onClick={() => setSelectedDate(date)}
              className={date === selectedDate ? 'active' : ''}
            >
              <span className="day-name">
                {new Date(date).toLocaleDateString('fr-FR', {
                  weekday: 'short'
                })}
              </span>
              <span className="date">
                {new Date(date).toLocaleDateString('fr-FR', {
                  day: 'numeric',
                  month: 'short'
                })}
              </span>
            </button>
          ))}
        </div>

        <div className="films-grid">
          {Object.values(seancesByFilm)
            .sort((a, b) => a.titre.localeCompare(b.titre, 'fr'))
            .map(film => (
              <div key={film.titre} className="film-card">
                <div className="film-poster-container">
                  {film.seances[0].poster ? (
                    <img 
                      src={film.seances[0].poster} 
                      alt={`Affiche ${film.titre}`} 
                      className="film-poster"
                    />
                  ) : (
                    <div className="film-poster-placeholder">
                      Pas d'affiche
                    </div>
                  )}
                </div>
                <div className="film-info">
                  <h3>{film.titre}</h3>
                  <div className="badges">
                    {film.duree && <span className="badge">{film.duree}</span>}
                    {film.genre && <span className="badge">{film.genre}</span>}
                  </div>
                  {film.synopsis && (
                    <p className="synopsis-preview">
                      {film.synopsis.slice(0, 100)}...
                    </p>
                  )}
                  <div className="seances-jour">
                    {Object.entries(
                      film.seances.reduce((acc, s) => {
                        if (s.jour.split('T')[0] === selectedDate) {
                          if (!acc[s.cinema]) acc[s.cinema] = [];
                          acc[s.cinema].push(s);
                        }
                        return acc;
                      }, {})
                    ).map(([cinema, seances]) => (
                      <div key={cinema} className="cinema-seances">
                        <h4>{cinema}</h4>
                        <div className="horaires">
                          {seances.map((s, i) => (
                            <span key={i} className="seance">
                              {s.heure} - {s.version}
                            </span>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                  <button 
                    className="voir-plus"
                    onClick={() => setSelectedFilm(film)}
                  >
                  </button>
                </div>
              </div>
            ))}
        </div>
      </main>

      {selectedFilm && (
        <FilmModal 
          film={selectedFilm} 
          onClose={() => setSelectedFilm(null)}
          isDarkMode={isDarkMode}
        />
      )}
    </div>
  );
};

export default SeancesViewer; 