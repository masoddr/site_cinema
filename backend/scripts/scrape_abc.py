import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.scrapers.abc import ABCScraper

def main():
    scraper = ABCScraper()
    scraper.save_to_json('abc_seances.json')
    print("Séances sauvegardées dans abc_seances.json")

if __name__ == "__main__":
    main() 