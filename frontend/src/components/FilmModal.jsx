import React from 'react';
import './FilmModal.css';

const FilmModal = ({ film, onClose, isDarkMode }) => {
  // Fermer si on clique en dehors du modal
  const handleBackdropClick = (e) => {
    if (e.target.className === 'modal-backdrop') {
      onClose();
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className={`modal-content ${isDarkMode ? 'dark-mode' : ''}`} onClick={e => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose}>×</button>
        <div className="modal-header">
          <h2>{film.titre}</h2>
        </div>
        <div className="modal-body">
          <div className="film-details">
            {film.seances[0].poster && (
              <img 
                src={film.seances[0].poster} 
                alt={`Affiche ${film.titre}`} 
                className="modal-poster"
              />
            )}
            <div className="film-info-modal">
              {film.duree && <p><strong>Durée :</strong> {film.duree}</p>}
              {film.genre && <p><strong>Genre :</strong> {film.genre}</p>}
              {film.synopsis && <p><strong>Synopsis :</strong> {film.synopsis}</p>}
            </div>
          </div>
          <div className="modal-seances">
            <h3>Séances disponibles :</h3>
            {film.seances.map((seance, index) => (
              <div key={index} className="seance-detail">
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