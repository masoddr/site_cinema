import logging
from datetime import datetime, date
import json
from .base_scraper import BaseScraper

try:
    from allocineAPI.allocineAPI import allocineAPI
except ImportError as e:
    logger = logging.getLogger(__name__)
    logger.error(f"Impossible d'importer allocineAPI: {e}")
    import requests
    class allocineAPI:
        def get_showtime(self, id_cinema, date_str):
            url = f"https://www.allocine.fr/_/showtimes/theater-{id_cinema}/{date_str}"
            response = requests.get(url)
            return response.json()

logger = logging.getLogger(__name__)

class AllocineScraper(BaseScraper):
    def __init__(self):
        self.cinemas = {
            'ABC': {
                'id': 'P0012',  # Peut-être que ces IDs ne sont plus valides ?
                'name': 'ABC'
            },
            'AMERICAN_COSMOGRAPH': {
                'id': 'P0235',
                'name': 'American Cosmograph'
            }
        }
        self.api = allocineAPI()

    def get_seances_cinema(self, cinema_id, cinema_name):
        logger.info(f"Récupération des séances pour {cinema_name}")
        
        try:
            today = date.today().strftime("%Y-%m-%d")
            logger.info(f"Requête API pour {cinema_name} (ID: {cinema_id}) à la date {today}")
            
            seances_data = self.api.get_showtime(cinema_id, today)
            
            if not seances_data:
                logger.error(f"Aucune donnée retournée par l'API pour {cinema_name}")
                return []

            seances = []
            
            # Format reçu : liste de films avec leurs séances
            for movie in seances_data:
                # Décoder proprement le titre avec les caractères spéciaux
                titre = movie.get('title', '')
                
                # Convertir les caractères encodés en UTF-8
                try:
                    titre = bytes(titre, 'latin1').decode('unicode-escape').encode('latin1').decode('utf-8')
                except Exception as e:
                    logger.warning(f"Erreur lors du décodage du titre '{titre}': {e}")
                
                # Pour chaque séance du film
                for seance in movie.get('showtimes', []):
                    try:
                        horaire = seance.get('startsAt')
                        version = seance.get('diffusionVersion', '')
                        
                        # Convertir le format de version
                        if version == 'ORIGINAL':
                            version = 'VO'
                        elif version in ['DUBBED', 'LOCAL']:
                            version = 'VF'
                        
                        dt = datetime.fromisoformat(horaire)
                        seances.append({
                            'titre': titre,
                            'heure': dt.strftime('%Hh%M'),
                            'jour': dt.replace(hour=0, minute=0, second=0, microsecond=0),
                            'cinema': cinema_name,
                            'version': version,
                            'duree': '',  # Non fourni dans cette réponse
                            'tags': []
                        })
                    except ValueError as e:
                        logger.error(f"Format d'horaire invalide {horaire}: {e}")
            
            logger.info(f"Nombre de séances trouvées : {len(seances)}")
            return seances
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des séances : {str(e)}")
            logger.exception("Détails de l'erreur:")
            return []

    def get_seances(self):
        """Récupère toutes les séances des deux cinémas"""
        all_seances = []
        
        for cinema in self.cinemas.values():
            seances = self.get_seances_cinema(cinema['id'], cinema['name'])
            all_seances.extend(seances)
            logger.info(f"Nombre de séances trouvées pour {cinema['name']}: {len(seances)}")

        return all_seances

    def save_to_json(self, filename='seances.json'):
        """Sauvegarde toutes les séances dans un fichier JSON"""
        seances = self.get_seances()
        
        # Convertir les dates en string pour le JSON
        for seance in seances:
            seance['jour'] = seance['jour'].isoformat()
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(seances, f, ensure_ascii=False, indent=2) 