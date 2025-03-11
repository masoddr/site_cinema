import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.scrapers.american_cosmograph import AmericanCosmographScraper
from app.scrapers.abc import ABCScraper
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Scraper l'American Cosmograph
    logger.info("Démarrage du scraping de l'American Cosmograph...")
    ac_scraper = AmericanCosmographScraper()
    ac_scraper.save_to_json('american_cosmograph_seances.json')
    
    # Scraper l'ABC
    logger.info("Démarrage du scraping de l'ABC...")
    abc_scraper = ABCScraper()
    abc_scraper.save_to_json('abc_seances.json')
    
    logger.info("Scraping terminé avec succès!")

if __name__ == "__main__":
    main() 