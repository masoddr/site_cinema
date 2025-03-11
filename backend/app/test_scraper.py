import logging
from scrapers.allocine import AllocineScraper

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    scraper = AllocineScraper()
    seances = scraper.get_seances()
    print(f"\nNombre total de séances récupérées : {len(seances)}")

if __name__ == "__main__":
    main() 