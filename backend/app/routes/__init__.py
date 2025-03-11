from flask import Blueprint, jsonify, current_app
from app.scrapers.allocine import AllocineScraper
from datetime import datetime

# Créer le blueprint
api = Blueprint('api', __name__)

@api.route('/test', methods=['GET'])
def test():
    return jsonify({'status': 'ok'})

@api.route('/seances', methods=['GET'])
def get_seances():
    try:
        scraper = AllocineScraper()
        seances = scraper.get_seances()
        
        # Convertir les dates en string pour JSON
        for seance in seances:
            if isinstance(seance['jour'], datetime):
                seance['jour'] = seance['jour'].isoformat()
        
        response = jsonify(seances)
        response.headers.add('Content-Type', 'application/json')
        return response
        
    except Exception as e:
        current_app.logger.error(f"Erreur: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Importer les routes après la création du blueprint
from . import cinema_routes 