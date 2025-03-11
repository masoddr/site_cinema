import logging
from datetime import datetime, date, timedelta
import json
from .base_scraper import BaseScraper
import requests
from bs4 import BeautifulSoup
import urllib.parse
import unicodedata

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
                'id': 'P0071',  # Mis à jour avec le bon ID
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

    def clean_title(self, title):
        """Nettoie et normalise le titre pour gérer les caractères spéciaux"""
        if isinstance(title, bytes):
            try:
                title = title.decode('utf-8')
            except UnicodeDecodeError:
                try:
                    title = title.decode('latin-1')
                except UnicodeDecodeError:
                    title = title.decode('utf-8', errors='ignore')
        
        # Normaliser les caractères spéciaux
        title = unicodedata.normalize('NFKC', str(title))
        return title

    def get_movie_details(self, movie_title):
        """Récupère les détails d'un film, y compris son affiche"""
        try:
            # Encoder le titre pour l'URL
            encoded_title = urllib.parse.quote(movie_title)
            
            # Essayer d'abord la recherche via l'API
            search_url = f"https://www.allocine.fr/rechercher/movie?q={encoded_title}"
            response = requests.get(search_url, headers=self.headers)
            
            logger.debug(f"URL de recherche: {search_url}")
            logger.debug(f"Status code: {response.status_code}")
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Essayer plusieurs sélecteurs pour trouver l'affiche
            poster_selectors = [
                '.thumbnail-img',
                '.entity-card-img img',
                '.mdl-card__media img',
                '.card-entity-list img',
                '.meta-title-thumbnail img',
                '.thumbnail img',
                'figure.thumbnail img',
                '.movie-card-poster img'
            ]
            
            # Essayer chaque sélecteur jusqu'à trouver une affiche
            for selector in poster_selectors:
                poster_elements = soup.select(selector)
                for poster_img in poster_elements:
                    # Vérifier si le titre du film correspond approximativement
                    alt_text = poster_img.get('alt', '').lower()
                    if movie_title.lower() in alt_text:
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
            
            # Si aucune affiche n'est trouvée, essayer une recherche plus générale
            fallback_url = f"https://www.allocine.fr/film/fichefilm_gen_cfilm={movie_title}.html"
            response = requests.get(fallback_url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            poster_img = soup.select_one('.poster-img')
            if poster_img:
                poster_url = poster_img.get('src')
                if poster_url:
                    if not poster_url.startswith('http'):
                        poster_url = f"https:{poster_url}"
                    logger.info(f"Affiche trouvée (fallback) pour '{movie_title}': {poster_url}")
                    return {'poster': poster_url}
            
            # Si toujours rien trouvé, utiliser une image par défaut
            logger.warning(f"Aucune affiche trouvée pour '{movie_title}'")
            return {'poster': 'https://www.allocine.fr/skin/img/placeholder/poster.jpg'}
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des détails du film '{movie_title}': {e}")
            return {'poster': 'https://www.allocine.fr/skin/img/placeholder/poster.jpg'}

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
            all_seances = []
            # Récupérer les séances pour aujourd'hui et les 6 prochains jours
            for i in range(7):
                current_date = (date.today() + timedelta(days=i)).strftime("%Y-%m-%d")
                logger.info(f"Requête API pour {cinema_name} (ID: {cinema_id}) à la date {current_date}")
                
                seances_data = self.api.get_showtime(cinema_id, current_date)
                
                if not seances_data:
                    logger.warning(f"Aucune donnée retournée par l'API pour {cinema_name} à la date {current_date}")
                    continue
                
                for movie in seances_data:
                    titre = movie.get('title', '')
                    
                    # On ne récupère l'affiche qu'une seule fois par film
                    if not any(s['titre'] == titre for s in all_seances):
                        # Chercher l'affiche sur la page du cinéma
                        poster_url = self.get_movie_poster_from_cinema_page(titre, cinema_id)
                        
                        # Si pas trouvé, essayer l'autre méthode
                        if not poster_url:
                            movie_details = self.get_movie_details(titre)
                            poster_url = movie_details.get('poster', '')
                        
                        logger.info(f"Film '{titre}' - URL de l'affiche: {poster_url}")
                    else:
                        # Réutiliser l'URL de l'affiche déjà trouvée
                        poster_url = next(s['poster'] for s in all_seances if s['titre'] == titre)

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
                            all_seances.append({
                                'titre': titre,
                                'heure': dt.strftime('%Hh%M'),
                                'jour': dt.replace(hour=0, minute=0, second=0, microsecond=0),
                                'cinema': cinema_name,
                                'version': version,
                                'duree': '',
                                'tags': [],
                                'poster': poster_url
                            })
                        except ValueError as e:
                            logger.error(f"Format d'horaire invalide {horaire}: {e}")
                
            logger.info(f"Nombre total de séances trouvées : {len(all_seances)}")

            # Ajouter après la boucle de récupération des séances
            missing_posters = set()
            for seance in all_seances:
                if not seance['poster']:
                    missing_posters.add(seance['titre'])

            if missing_posters:
                logger.warning(f"Films sans affiche pour {cinema_name}: {', '.join(missing_posters)}")

            return all_seances
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des séances : {str(e)}")
            logger.exception("Détails de l'erreur:")
            return []

    def get_seances(self):
        try:
            seances = []
            for cinema_id, cinema_info in self.cinemas.items():
                cinema_seances = self.get_seances_cinema(
                    cinema_info['id'], 
                    cinema_info['name']
                )
                for seance in cinema_seances:
                    seance['titre'] = self.clean_title(seance['titre'])
                seances.extend(cinema_seances)
            return seances
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des séances: {e}")
            return []

    def save_to_json(self, filename='seances.json'):
        """Sauvegarde toutes les séances dans un fichier JSON"""
        seances = self.get_seances()
        
        # Convertir les dates en string pour le JSON
        for seance in seances:
            seance['jour'] = seance['jour'].isoformat()
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(seances, f, ensure_ascii=False, indent=2) 