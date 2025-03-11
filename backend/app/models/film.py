from . import db
from datetime import datetime, UTC

class Film(db.Model):
    __tablename__ = 'films'
    
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(200), nullable=False)
    synopsis = db.Column(db.Text)
    duree = db.Column(db.Integer)  # durée en minutes
    realisateur = db.Column(db.String(100))
    annee = db.Column(db.Integer)
    langue = db.Column(db.String(50))
    sous_titres = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))
    
    # Relation avec les séances
    seances = db.relationship('Seance', back_populates='film', lazy='dynamic',
                             cascade="all, delete")
    
    def __repr__(self):
        return f'<Film {self.titre}>' 