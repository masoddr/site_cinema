from app.scrapers.allocine import AllocineScraper
from app.cache_manager import SeancesCacheManager
from app.config import Config

def init_cache():
    scraper = AllocineScraper()
    seances = scraper.get_seances()
    
    cache_manager = SeancesCacheManager(Config.SEANCES_CACHE_FILE)
    cache_manager.update_cache(seances)
    
    print(f"Cache initialisé avec succès dans {Config.SEANCES_CACHE_FILE}!")

if __name__ == "__main__":
    init_cache() 