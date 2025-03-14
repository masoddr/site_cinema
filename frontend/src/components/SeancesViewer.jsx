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
  const [searchTerm, setSearchTerm] = useState('');
  const [showNextHour, setShowNextHour] = useState(false);

  const cinemas = [...new Set(seances.map(s => s.cinema))];

  // Ajouter un objet pour définir les couleurs des cinémas avec des couleurs plus vives
  const cinemaColors = {
    'Le Palace': '#FF0000', // Rouge vif
    'Cinéma Lumière': '#00FF00', // Vert vif
    'Ciné Paradiso': '#0000FF', // Bleu vif
    'Mégarama': '#FFD700', // Or
    'UGC': '#FF00FF' // Magenta
  };

  // Fonction pour obtenir une couleur par défaut si le cinéma n'est pas dans la liste
  const getCinemaColor = (cinema) => {
    return cinemaColors[cinema] || '#888888';
  };

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

  // Fonction pour vérifier si une séance est dans l'heure qui suit
  const isWithinNextHour = (heure) => {
    const now = new Date();
    const [hours, minutes] = heure.split(':').map(Number);
    const seanceTime = new Date(now);
    seanceTime.setHours(hours, minutes, 0);
    
    const diffMs = seanceTime - now;
    const diffMinutes = diffMs / (1000 * 60);
    
    return diffMinutes > 0 && diffMinutes <= 60;
  };

  // Modifier seancesByFilm pour inclure le filtrage par heure
  const seancesByFilm = seances.reduce((acc, seance) => {
    if (
      seance.jour.split('T')[0] === selectedDate && 
      selectedCinemas.has(seance.cinema) &&
      seance.titre.toLowerCase().includes(searchTerm.toLowerCase()) &&
      (!showNextHour || isWithinNextHour(seance.heure))
    ) {
      if (!acc[seance.titre]) {
        acc[seance.titre] = {
          titre: seance.titre,
          duree: seance.duree,
          date_sortie: seance.date_sortie,
          note: seance.note,
          tmdb_id: seance.tmdb_id,
          poster: seance.poster,
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
          <div className="quick-filters">
            <button 
              className={`quick-filter-btn ${showNextHour ? 'active' : ''}`}
              onClick={() => setShowNextHour(true)}
            >
              🕐 Un film dans moins d'1h !
            </button>
            <button 
              className="quick-filter-btn"
              onClick={() => setShowNextHour(false)}
            >
              Toutes les séances
            </button>
          </div>
          <div className="search-bar">
            <input
              type="text"
              placeholder="Rechercher un film..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="search-input"
            />
            {searchTerm && (
              <button 
                className="clear-search"
                onClick={() => setSearchTerm('')}
                title="Effacer la recherche"
              >
                ×
              </button>
            )}
          </div>
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
            <label 
              className="switch"
              title={isDarkMode ? "Passer en mode clair" : "Passer en mode sombre"}
            >
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
                    {film.duree && (
                      <span className="badge">
                        {Math.floor(film.duree / 60)}h{film.duree % 60}min
                      </span>
                    )}
                    {film.date_sortie && (
                      <span className="badge">
                        Sortie : {new Date(film.date_sortie).toLocaleDateString('fr-FR')}
                      </span>
                    )}
                    {film.note && (
                      <span className="badge" title="Note TMDb">
                        ⭐ {film.note.toFixed(1)}/10
                      </span>
                    )}
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
                      <div 
                        key={cinema} 
                        className="cinema-seances"
                        style={{
                          borderLeft: `8px solid ${getCinemaColor(cinema)}`,
                          backgroundColor: `${getCinemaColor(cinema)}88`,
                          padding: '12px',
                          margin: '8px 0',
                          borderRadius: '8px',
                          boxShadow: `0 2px 4px ${getCinemaColor(cinema)}88`
                        }}
                      >
                        <h4 style={{ 
                          color: isDarkMode ? '#FFFFFF' : getCinemaColor(cinema),
                          fontWeight: 'bold',
                          fontSize: '1.1em'
                        }}>
                          {cinema}
                        </h4>
                        <div className="horaires">
                          {seances.map((s, i) => (
                            <span 
                              key={i} 
                              className={`seance ${isWithinNextHour(s.heure) ? 'next-hour' : ''}`}
                              style={{
                                backgroundColor: `${getCinemaColor(cinema)}AA`,
                                border: `2px solid ${getCinemaColor(cinema)}`,
                                color: isDarkMode ? '#FFFFFF' : '#000000',
                                fontWeight: 'bold',
                                padding: '8px 12px',
                                margin: '4px',
                                display: 'inline-block',
                                boxShadow: isWithinNextHour(s.heure) ? '0 0 15px rgba(255, 255, 0, 0.5)' : 'none'
                              }}
                            >
                              {s.heure} - {s.version}
                            </span>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                  <button 
                    className="voir-plus-btn"
                    onClick={() => setSelectedFilm(film)}
                  >
                    Voir plus
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