import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import logging
import time
from .base_scraper import BaseScraper

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ABCScraper(BaseScraper):
    BASE_URL = "https://abc-toulouse.fr/horaires.html"
    CINEMA = "ABC"

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
        time.sleep(2)  # Respecter le site
        response = requests.get(self.BASE_URL, headers=self.HEADERS)
        logger.info(f"Statut de la réponse : {response.status_code}")

        if response.status_code != 200:
            logger.error(f"Erreur lors de la récupération des séances : {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Debug: Sauvegarder le HTML pour inspection
        with open('debug_abc.html', 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
        
        seances = []
        # Trouver tous les films
        films = soup.find_all('div', class_='layout_filminfos')
        logger.debug(f"Nombre de films trouvés : {len(films)}")
        
        for film in films:
            # Extraire le titre
            titre_element = film.find('h2')
            titre = titre_element.text.strip() if titre_element else "Inconnu"
            logger.debug(f"Film trouvé : {titre}")
            
            # Extraire la durée
            duree_element = film.find('div', class_='field group1')
            duree = duree_element.text.strip().split('/')[0].strip() if duree_element else ""
            
            # Trouver les horaires du film
            horaires = film.find_next('div', class_='filmhoraires')
            if not horaires:
                continue
            
            # Pour chaque jour
            for sdate in horaires.find_all('div', class_='sdate'):
                # Extraire la date
                day = sdate.find('div', class_='day').text.strip()
                month = sdate.find('div', class_='month').text.strip()
                # Extraire le jour du mois (11)
                jour_num = day.split()[-1]  # Prend le dernier mot de "Mardi 11"
                
                # Convertir le mois en anglais
                mois_fr_to_en = {
                    'janvier': 'January',
                    'février': 'February',
                    'mars': 'March',
                    'avril': 'April',
                    'mai': 'May',
                    'juin': 'June',
                    'juillet': 'July',
                    'août': 'August',
                    'septembre': 'September',
                    'octobre': 'October',
                    'novembre': 'November',
                    'décembre': 'December'
                }
                
                # Extraire le mois et l'année
                mois, annee = month.split()
                mois_en = mois_fr_to_en.get(mois.lower(), mois)
                
                # Combiner avec le mois et l'année
                date_str = f"{jour_num} {mois_en} {annee}"  # "11 March 2025"
                try:
                    jour = datetime.strptime(date_str, '%d %B %Y')
                    # Réinitialiser l'heure à minuit
                    jour = jour.replace(hour=0, minute=0, second=0, microsecond=0)
                except ValueError:
                    logger.error(f"Format de date non reconnu : {date_str}")
                    # En cas d'erreur, on continue avec la prochaine séance
                    continue
                
                # Pour chaque séance de ce jour
                for session in sdate.find_all('a', class_='session'):
                    heure = session.find('div', class_='stime').text.strip()
                    # Convertir le format de l'heure de "13:50" à "13h50"
                    heure = heure.replace(':', 'h')
                    version = session.find('div', class_='version').text.strip()
                    salle = session.find('div', class_='room').text.strip()
                    
                    seances.append({
                        'titre': titre,
                        'heure': heure,
                        'jour': jour,
                        'cinema': self.CINEMA,
                        'salle': salle,
                        'duree': duree,
                        'version': version,
                        'tags': []
                    })
        
        logger.info(f"Nombre total de séances trouvées : {len(seances)}")
        return seances

    def save_to_json(self, filename='abc_seances.json'):
        """Sauvegarde les séances dans un fichier JSON"""
        seances = self.get_seances()
        
        # Convertir les dates en string pour le JSON
        for seance in seances:
            seance['jour'] = seance['jour'].isoformat()
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(seances, f, ensure_ascii=False, indent=2) 