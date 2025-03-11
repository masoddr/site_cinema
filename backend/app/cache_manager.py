import json
import os
import time
from datetime import datetime
from flask import current_app
import logging

logger = logging.getLogger(__name__)

class SeancesCacheManager:
    def __init__(self, cache_file):
        self.cache_file = cache_file
        self.cache_dir = os.path.dirname(cache_file)
        
        # Créer le dossier data s'il n'existe pas
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

    def get_cache(self):
        """Récupère les données du cache si elles sont valides"""
        try:
            if not os.path.exists(self.cache_file):
                return None

            with open(self.cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)

            # Vérifier si le cache est périmé
            last_update = datetime.fromisoformat(cache_data['last_update'])
            cache_age = (datetime.now() - last_update).total_seconds() / 3600  # en heures
            
            if cache_age < current_app.config['SCRAPING_INTERVAL']:
                logger.info("Utilisation du cache des séances")
                return cache_data['seances']
                
            logger.info("Cache périmé, nouvelle récupération nécessaire")
            return None

        except Exception as e:
            logger.error(f"Erreur lors de la lecture du cache : {e}")
            return None

    def update_cache(self, seances):
        """Met à jour le cache avec les nouvelles données"""
        try:
            # Convertir les dates en string pour la sérialisation JSON
            seances_json = []
            for seance in seances:
                seance_copy = seance.copy()
                if isinstance(seance_copy.get('jour'), datetime):
                    seance_copy['jour'] = seance_copy['jour'].isoformat()
                seances_json.append(seance_copy)

            cache_data = {
                'last_update': datetime.now().isoformat(),
                'seances': seances_json
            }
            
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
                
            logger.info("Cache des séances mis à jour")
            
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour du cache : {e}") 