import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.scrapers.allocine import AllocineScraper
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Scraper Allociné pour les deux cinémas
    logger.info("Démarrage du scraping Allociné...")
    scraper = AllocineScraper()
    scraper.save_to_json('seances.json')
    logger.info("Scraping terminé avec succès!")

if __name__ == "__main__":
    main() 