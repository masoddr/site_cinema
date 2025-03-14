import React from 'react';
import './FilmModal.css';

const FilmModal = ({ film, onClose, isDarkMode }) => {
  return (
    <div className={`modal-overlay ${isDarkMode ? 'dark-mode' : ''}`} onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <div className="modal-poster">
            {film.poster ? (
              <img src={film.poster} alt={`Affiche ${film.titre}`} />
            ) : (
              <div className="poster-placeholder">Pas d'affiche</div>
            )}
          </div>
          
          <div className="modal-title">
            <h2>{film.titre}</h2>
            <div className="film-metadata">
              {film.duree && (
                <span className="metadata-item">
                  ⏱️ {Math.floor(film.duree / 60)}h{film.duree % 60}min
                </span>
              )}
              {film.date_sortie && (
                <span className="metadata-item">
                  📅 Sortie le {new Date(film.date_sortie).toLocaleDateString('fr-FR', {
                    day: 'numeric',
                    month: 'long',
                    year: 'numeric'
                  })}
                </span>
              )}
              {film.note && (
                <span className="metadata-item">
                  ⭐ Note TMDb : {film.note.toFixed(1)}/10
                </span>
              )}
            </div>
          </div>
        </div>

        <div className="modal-body">
          <h3>Séances disponibles</h3>
          <div className="seances-list">
            {film.seances.map((seance, index) => (
              <div key={index} className="seance-item">
                <span className="cinema">{seance.cinema}</span>
                <span className="horaire">{seance.heure}</span>
                <span className="version">{seance.version}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default FilmModal; 