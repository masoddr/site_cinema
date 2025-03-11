from . import db
from datetime import datetime, UTC

class Seance(db.Model):
    __tablename__ = 'seances'
    
    id = db.Column(db.Integer, primary_key=True)
    date_heure = db.Column(db.DateTime, nullable=False)
    prix = db.Column(db.Float)
    langue = db.Column(db.String(50))  # Peut être différent du film original
    sous_titres = db.Column(db.String(50))  # Peut varier selon la séance
    
    # Clés étrangères
    film_id = db.Column(db.Integer, db.ForeignKey('films.id', ondelete='CASCADE'), nullable=False)
    cinema_id = db.Column(db.Integer, db.ForeignKey('cinemas.id'), nullable=False)
    
    # Relations
    film = db.relationship('Film', back_populates='seances')
    cinema = db.relationship('Cinema', back_populates='seances')
    
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))
    
    def __repr__(self):
        return f'<Seance {self.film.titre} - {self.date_heure}>' 