import React from 'react';
import './FilmModal.css';

const FilmModal = ({ film, onClose }) => {
  // Fermer si on clique en dehors du modal
  const handleBackdropClick = (e) => {
    if (e.target.className === 'modal-backdrop') {
      onClose();
    }
  };

  return (
    <div className="modal-backdrop" onClick={handleBackdropClick}>
      <div className="modal-content">
        <div className="modal-header">
          <h2>{film.titre}</h2>
          <button className="close-button" onClick={onClose}>&times;</button>
        </div>
        
        <div className="modal-body">
          <div className="film-details">
            <img src={film.seances[0].poster} alt={film.titre} className="modal-poster" />
            <div className="film-info-modal">
              <div className="badges">
                {film.duree && <span className="badge">{film.duree}</span>}
                {film.genre && <span className="badge">{film.genre}</span>}
              </div>
              {film.synopsis && <p className="synopsis">{film.synopsis}</p>}
            </div>
          </div>

          <div className="seances-completes">
            <h3>Toutes les séances</h3>
            {Object.entries(film.seances.reduce((acc, s) => {
              if (!acc[s.cinema]) acc[s.cinema] = [];
              acc[s.cinema].push(s);
              return acc;
            }, {})).map(([cinema, seances]) => (
              <div key={cinema} className="cinema-section">
                <h4>{cinema}</h4>
                <div className="horaires-grid">
                  {seances.map((s, i) => (
                    <div key={i} className="seance-detail">
                      <span className="jour">{new Date(s.jour).toLocaleDateString('fr-FR', { weekday: 'long', day: 'numeric', month: 'long' })}</span>
                      <span className="heure">{s.heure}</span>
                      <span className="version">{s.version}</span>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default FilmModal; 