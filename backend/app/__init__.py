from flask import Flask
from flask_cors import CORS
from .config import Config
from app.models import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialisation des extensions
    CORS(app)
    db.init_app(app)
    
    # Création des tables au démarrage
    with app.app_context():
        db.create_all()
    
    # Ici nous importerons plus tard nos routes
    from app.routes import main
    app.register_blueprint(main)
    
    @app.route('/health')
    def health_check():
        return {'status': 'ok'}, 200
        
    return app
