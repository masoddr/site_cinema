import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import logging
import time
from .base_scraper import BaseScraper

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class AmericanCosmographScraper(BaseScraper):
    BASE_URL = "https://www.american-cosmograph.fr/les-horaires.html"
    CINEMA = "American Cosmograph"

    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

    def get_seances(self):
        """Récupère toutes les séances du cinéma"""
        logger.info(f"Récupération des séances depuis {self.BASE_URL}")
        time.sleep(2)
        response = requests.get(self.BASE_URL, headers=self.HEADERS)
        logger.info(f"Statut de la réponse : {response.status_code}")

        if response.status_code != 200:
            logger.error(f"Erreur lors de la récupération des séances : {response.status_code}")
            logger.debug(f"Contenu de la réponse : {response.text[:500]}...")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Debug: Sauvegarder le HTML pour inspection
        with open('debug_page.html', 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
        
        seances = []
        # Trouver tous les conteneurs de séances (un par jour)
        seances_containers = soup.find_all('div', class_='tab-pane', attrs={'id': lambda x: x and x.startswith('seance-')})
        logger.info(f"Nombre de jours trouvés : {len(seances_containers)}")
        
        for seances_container in seances_containers:
            # Extraire la date du conteneur
            date_str = seances_container.get('id').replace('seance-', '')
            jour = datetime.strptime(date_str, '%Y-%m-%d')
            logger.info(f"Traitement des séances pour le {jour.strftime('%d/%m/%Y')}")
            
            # Trouver toutes les séances pour ce jour
            for li in seances_container.find_all('li', class_='heureReady'):
                # Trouver le titre du film
                titre_element = li.find('div', class_='filmTitle').find('a')
                titre = titre_element.text.strip() if titre_element else "Inconnu"
                logger.debug(f"Film trouvé : {titre}")
                
                # Extraire l'heure
                heure_element = li.find('span', class_='horaire_debut')
                if heure_element:
                    heure = heure_element.text.strip().replace('Début du film :', '').strip()
                    logger.debug(f"Heure trouvée : {heure}")
                
                # Extraire la salle
                salle_element = li.find('div', class_='horaire').find(text=lambda t: t and 'salle' in t.lower())
                salle = salle_element.strip() if salle_element else ""
                
                # Extraire la durée
                duree_element = li.find('div', class_='horaire').find(text=lambda t: t and 'Durée :' in t)
                duree = duree_element.replace('Durée :', '').strip() if duree_element else ""
                
                # Extraire les tags (VO, événement, tarif réduit, etc.)
                tags = []
                tags_container = li.find('div', class_='filmTags')
                if tags_container:
                    for tag in tags_container.find_all('div'):
                        tags.append(tag.text.strip())
                
                seances.append({
                    'titre': titre,
                    'heure': heure,
                    'jour': jour,
                    'cinema': self.CINEMA,
                    'salle': salle,
                    'duree': duree,
                    'tags': tags
                })

        logger.info(f"Nombre total de séances trouvées : {len(seances)}")
        return seances

    def save_to_json(self, filename='seances.json'):
        """Sauvegarde les séances dans un fichier JSON"""
        seances = self.get_seances()
        
        # Convertir les dates en string pour le JSON
        for seance in seances:
            seance['jour'] = seance['jour'].isoformat()
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(seances, f, ensure_ascii=False, indent=2) 