#!/usr/bin/env python
import os
import sys
from pathlib import Path
import json
import logging

# Ajouter le répertoire parent au PYTHONPATH
sys.path.append(str(Path(__file__).parent.parent))

from allocineAPI.allocineAPI import allocineAPI
from datetime import date

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_abc_real_pain():
    api = allocineAPI()
    cinema_id = 'P0012'  # ID de l'ABC
    today = date.today().strftime("%Y-%m-%d")
    
    logger.info(f"Test de l'API pour ABC (ID: {cinema_id}) à la date {today}")
    
    # Récupérer les données brutes de l'API
    response = api.get_showtime(cinema_id, today)
    
    # Sauvegarder la réponse complète pour inspection
    with open('api_response_abc.json', 'w', encoding='utf-8') as f:
        json.dump(response, f, ensure_ascii=False, indent=2)
    
    # Chercher spécifiquement "A Real Pain"
    for movie in response:
        if movie.get('title') == 'A Real Pain':
            logger.info("\nDonnées pour 'A Real Pain':")
            logger.info(json.dumps(movie, ensure_ascii=False, indent=2))
            
            logger.info("\nSéances:")
            for seance in movie.get('showtimes', []):
                logger.info(f"- {seance.get('startsAt')} ({seance.get('diffusionVersion')})")

if __name__ == "__main__":
    test_abc_real_pain() 