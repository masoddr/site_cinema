import logging
from datetime import datetime, date
import json
from .base_scraper import BaseScraper
import requests
from bs4 import BeautifulSoup
import urllib.parse

try:
    from allocineAPI.allocineAPI import allocineAPI
except ImportError as e:
    logger = logging.getLogger(__name__)
    logger.error(f"Impossible d'importer allocineAPI: {e}")
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
        self.base_url = "https://www.allocine.fr"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def get_movie_details(self, movie_title):
        """Récupère les détails d'un film, y compris son affiche"""
        try:
            # Encoder le titre pour l'URL
            encoded_title = urllib.parse.quote(movie_title)
            
            # Utiliser l'API de recherche d'Allociné
            search_url = f"{self.base_url}/recherche/1/?q={encoded_title}"
            response = requests.get(search_url, headers=self.headers)
            
            # Log pour debug
            logger.debug(f"URL de recherche: {search_url}")
            logger.debug(f"Status code: {response.status_code}")
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Chercher l'image dans différents sélecteurs possibles
            poster_selectors = [
                'img.thumbnail-img',
                '.thumbnail-img',
                '.entity-card-img img',
                '.mdl-card__media img',
                '.card-entity-list img'
            ]
            
            for selector in poster_selectors:
                poster_img = soup.select_one(selector)
                if poster_img:
                    # Log pour debug
                    logger.debug(f"Trouvé avec le sélecteur: {selector}")
                    logger.debug(f"Attributs de l'image: {poster_img.attrs}")
                    
                    # Essayer différents attributs pour l'URL
                    poster_url = (
                        poster_img.get('data-src') or
                        poster_img.get('src') or
                        poster_img.get('content')
                    )
                    
                    if poster_url:
                        # Convertir en haute qualité si possible
                        poster_url = poster_url.replace('c_160_213', 'c_310_420')
                        poster_url = poster_url.replace('r_160_213', 'r_310_420')
                        
                        # S'assurer que l'URL est absolue
                        if not poster_url.startswith('http'):
                            poster_url = f"https:{poster_url}"
                        
                        logger.info(f"Affiche trouvée pour '{movie_title}': {poster_url}")
                        return {'poster': poster_url}
            
            logger.warning(f"Aucune affiche trouvée pour '{movie_title}'")
            return {'poster': ''}
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des détails du film '{movie_title}': {e}")
            return {'poster': ''}

    def get_movie_poster_from_cinema_page(self, movie_title, cinema_id):
        """Récupère l'affiche d'un film depuis la page du cinéma"""
        try:
            # URL de la page du cinéma sur Allociné
            cinema_url = f"{self.base_url}/seance/salle_gen_csalle={cinema_id}.html"
            response = requests.get(cinema_url, headers=self.headers)
            
            if response.status_code != 200:
                logger.warning(f"Impossible d'accéder à la page du cinéma: {cinema_url}")
                return None
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Chercher l'image du film par son titre
            movie_elements = soup.find_all('span', {'class': 'thumbnail-container'})
            for element in movie_elements:
                if element.get('title') == movie_title:
                    img = element.find('img', {'class': 'thumbnail-img'})
                    if img and 'data-src' in img.attrs:
                        poster_url = img['data-src']
                        # Convertir en haute qualité
                        poster_url = poster_url.replace('c_160_213', 'c_310_420')
                        logger.info(f"Affiche trouvée pour '{movie_title}': {poster_url}")
                        return poster_url
            
            logger.warning(f"Pas d'affiche trouvée pour '{movie_title}' sur la page du cinéma")
            return None
            
        except Exception as e:
            logger.error(f"Erreur lors de la recherche de l'affiche pour '{movie_title}': {e}")
            return None

    def get_seances_cinema(self, cinema_id, cinema_name):
        logger.info(f"Récupération des séances pour {cinema_name}")
        
        try:
            today = date.today().strftime("%Y-%m-%d")
            logger.info(f"Requête API pour {cinema_name} (ID: {cinema_id}) à la date {today}")
            
            seances_data = self.api.get_showtime(cinema_id, today)
            
            # Log de la réponse API complète pour voir la structure
            logger.info(f"Structure de la réponse API pour un film :\n{json.dumps(seances_data[0] if seances_data else {}, indent=2)}")
            
            if not seances_data:
                logger.error(f"Aucune donnée retournée par l'API pour {cinema_name}")
                return []

            seances = []
            
            for movie in seances_data:
                titre = movie.get('title', '')
                
                # Chercher l'affiche sur la page du cinéma
                poster_url = self.get_movie_poster_from_cinema_page(titre, cinema_id)
                
                # Si pas trouvé, essayer l'autre méthode
                if not poster_url:
                    movie_details = self.get_movie_details(titre)
                    poster_url = movie_details.get('poster', '')
                
                logger.info(f"Film '{titre}' - URL de l'affiche: {poster_url}")
                
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
                            'tags': [],
                            'poster': poster_url  # Ajout de l'URL de l'affiche
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