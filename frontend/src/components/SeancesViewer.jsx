import React, { useState } from 'react';
import FilmModal from './FilmModal';
import './SeancesViewer.css';

const SeancesViewer = ({ seances }) => {
  const [selectedDate, setSelectedDate] = useState(
    seances.length > 0 ? seances[0].jour.split('T')[0] : null
  );
  const [selectedFilm, setSelectedFilm] = useState(null);

  // Grouper les séances par film pour la date sélectionnée
  const seancesByFilm = seances.reduce((acc, seance) => {
    if (seance.jour.split('T')[0] === selectedDate) {
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

  // Obtenir les dates uniques pour le sélecteur
  const dates = [...new Set(seances.map(s => s.jour.split('T')[0]))];

  return (
    <div className="seances-viewer">
      <div className="date-selector">
        {dates.map(date => (
          <button
            key={date}
            onClick={() => setSelectedDate(date)}
            className={date === selectedDate ? 'active' : ''}
          >
            {new Date(date).toLocaleDateString('fr-FR', {
              weekday: 'long',
              day: 'numeric',
              month: 'long'
            })}
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
                  Voir plus
                </button>
              </div>
            </div>
          ))}
      </div>

      {selectedFilm && (
        <FilmModal 
          film={selectedFilm} 
          onClose={() => setSelectedFilm(null)}
        />
      )}
    </div>
  );
};

export default SeancesViewer; 