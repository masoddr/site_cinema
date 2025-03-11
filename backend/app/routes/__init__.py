from flask import Blueprint, jsonify, current_app
from app.scrapers.allocine import AllocineScraper
from app.cache_manager import SeancesCacheManager
from datetime import datetime

# Créer le blueprint
api = Blueprint('api', __name__)

@api.route('/test', methods=['GET'])
def test():
    return jsonify({'status': 'ok'})

@api.route('/seances', methods=['GET'])
def get_seances():
    try:
        if not current_app.config.get('SEANCES_CACHE_FILE'):
            raise ValueError("Configuration SEANCES_CACHE_FILE manquante")
            
        cache_manager = SeancesCacheManager(current_app.config['SEANCES_CACHE_FILE'])
        seances = cache_manager.get_cache()
        
        if seances is None:
            scraper = AllocineScraper()
            seances = scraper.get_seances()
            cache_manager.update_cache(seances)
        
        response = jsonify(seances)
        response.headers.add('Content-Type', 'application/json')
        return response
        
    except Exception as e:
        current_app.logger.error(f"Erreur: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Importer les routes après la création du blueprint
from . import cinema_routes 