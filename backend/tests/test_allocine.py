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
    
    # Récupérer les séances
    seances = scraper.get_seances()
    
    # Vérifications basiques
    assert len(seances) > 0, "Aucune séance trouvée"
    
    # Vérifier la structure d'une séance
    for seance in seances:
        assert all(key in seance for key in [
            'titre', 'heure', 'jour', 'cinema', 'salle', 'duree', 'version', 'tags'
        ]), f"Structure invalide pour la séance : {seance}"
        
        # Vérifier que le cinéma est soit ABC soit American Cosmograph
        assert seance['cinema'] in ['ABC', 'American Cosmograph'], \
            f"Cinéma invalide : {seance['cinema']}"
        
        # Vérifier le format de l'heure (13h50)
        assert 'h' in seance['heure'], \
            f"Format d'heure invalide : {seance['heure']}"
    
    # Sauvegarder en JSON pour inspection
    test_file = 'test_allocine_seances.json'
    scraper.save_to_json(test_file)
    
    # Charger et vérifier que le JSON est valide
    with open(test_file, 'r', encoding='utf-8') as f:
        loaded_seances = json.load(f)
        assert len(loaded_seances) == len(seances), "Perte de données lors de la sauvegarde JSON"
    
    # Afficher quelques statistiques
    cinemas = {}
    for seance in seances:
        cinema = seance['cinema']
        if cinema not in cinemas:
            cinemas[cinema] = 0
        cinemas[cinema] += 1
    
    logger.info("=== Résultats du test ===")
    logger.info(f"Nombre total de séances : {len(seances)}")
    for cinema, count in cinemas.items():
        logger.info(f"Séances pour {cinema} : {count}")
    logger.info(f"Données sauvegardées dans {test_file}")
    
    # Afficher quelques exemples de séances
    logger.info("\n=== Exemples de séances ===")
    for i, seance in enumerate(seances[:3]):
        logger.info(f"Séance {i+1}:")
        logger.info(json.dumps(seance, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    test_allocine_scraper() 