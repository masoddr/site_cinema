from . import db
from datetime import datetime, UTC

class Cinema(db.Model):
    __tablename__ = 'cinemas'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    adresse = db.Column(db.String(255))
    site_web = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC), 
                          onupdate=lambda: datetime.now(UTC))

    # Relation avec les séances
    seances = db.relationship('Seance', back_populates='cinema', lazy='dynamic')

    def __repr__(self):
        return f'<Cinema {self.nom}>' 