import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.scrapers.allocine import AllocineScraper
import logging
import json
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_allocine_scraper():
    # Initialiser le scraper
    scraper = AllocineScraper()
    
    # Test pour chaque cinéma
    for cinema_id, cinema_info in scraper.cinemas.items():
        logger.info(f"\nTest du scraping pour {cinema_info['name']}:")
        seances = scraper.get_seances_cinema(cinema_info['id'], cinema_info['name'])
        
        if not seances:
            logger.error(f"❌ Aucune séance trouvée pour {cinema_info['name']}")
            continue
            
        logger.info(f"✅ {len(seances)} séances trouvées")
        
        # Afficher un exemple de séance
        if seances:
            logger.info("\nExemple de séance:")
            logger.info(json.dumps(seances[0], ensure_ascii=False, default=str, indent=2))
            
            # Vérifier le format des données
            seance = seances[0]
            assert all(key in seance for key in ['titre', 'heure', 'jour', 'cinema', 'version', 'duree'])
            assert 'h' in seance['heure']
            assert isinstance(seance['jour'], datetime)
    
    # Tester la sauvegarde en JSON
    test_file = 'test_seances.json'
    logger.info(f"\nTest de la sauvegarde dans {test_file}")
    
    try:
        scraper.save_to_json(test_file)
        
        # Vérifier que le fichier est bien créé et lisible
        with open(test_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            logger.info(f"✅ Fichier JSON créé avec succès ({len(data)} séances)")
            
    except Exception as e:
        logger.error(f"❌ Erreur lors de la sauvegarde : {str(e)}")

def test_movie_details():
    """Test la récupération des affiches pour quelques films"""
    scraper = AllocineScraper()
    
    # Liste de films à tester
    films = [
        "Mickey 17",
        "The Brutalist",
        "Yōkai - le monde des esprits",
        "L'Énigme Velázquez"
    ]
    
    logger.info("\nTest de récupération des affiches:")
    for titre in films:
        details = scraper.get_movie_details(titre)
        if details['poster']:
            logger.info(f"✅ {titre}: {details['poster']}")
        else:
            logger.error(f"❌ {titre}: Pas d'affiche trouvée")

def test_seances_avec_affiches():
    """Test la récupération des séances avec leurs affiches"""
    scraper = AllocineScraper()
    seances = scraper.get_seances()
    
    # Regrouper par film pour éviter les doublons
    films_uniques = {}
    for seance in seances:
        if seance['titre'] not in films_uniques:
            films_uniques[seance['titre']] = seance['poster']
    
    logger.info("\nAffiches trouvées:")
    for titre, poster in films_uniques.items():
        if poster:
            logger.info(f"✅ {titre}: {poster}")
        else:
            logger.warning(f"⚠️ {titre}: Pas d'affiche")

if __name__ == "__main__":
    test_allocine_scraper()
    test_movie_details()
    test_seances_avec_affiches() 