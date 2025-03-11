import os
import sys

# Ajouter le dossier parent (backend) au PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.scrapers.american_cosmograph import AmericanCosmographScraper

def main():
    scraper = AmericanCosmographScraper()
    scraper.save_to_json('american_cosmograph_seances.json')
    print("Séances sauvegardées dans american_cosmograph_seances.json")

if __name__ == "__main__":
    main() 