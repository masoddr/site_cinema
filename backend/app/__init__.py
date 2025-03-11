from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from dotenv import load_dotenv
from .config import Config  # Importons la classe Config

load_dotenv()

db = SQLAlchemy()

def create_app(config_class=Config):  # Ajout du paramètre config_class
    app = Flask(__name__)
    
    # Utiliser la configuration depuis la classe Config
    app.config.from_object(config_class)
    
    # Configuration CORS simplifiée pour le développement
    CORS(app, resources={
        r"/*": {
            "origins": "*",
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type"]
        }
    })
    
    db.init_app(app)
    
    # Importer et enregistrer les routes
    from app.routes import api
    app.register_blueprint(api, url_prefix='/api')
    
    # Créer le dossier data s'il n'existe pas
    os.makedirs(os.path.join(os.path.dirname(app.root_path), 'data'), exist_ok=True)
    
    return app
