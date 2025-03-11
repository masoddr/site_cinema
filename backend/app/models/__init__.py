# Ce fichier sera utilisé pour les imports des modèles
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
Base = declarative_base()

# Import des modèles pour que Flask-SQLAlchemy les connaisse
from .cinema import Cinema
from .film import Film
from .seance import Seance 