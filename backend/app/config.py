import os
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

class Config:
    # Configuration Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-à-changer-en-prod'
    
    # Configuration Base de données
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://user:password@localhost:5432/cinema_toulouse'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuration Scraping
    SCRAPING_INTERVAL = int(os.environ.get('SCRAPING_INTERVAL', 168))
    
    # Chemin vers le fichier de cache des séances
    SEANCES_CACHE_FILE = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'data',
        'seances_cache.json'
    )

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
