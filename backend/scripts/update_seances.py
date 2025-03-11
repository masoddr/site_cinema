#!/usr/bin/env python
import os
import sys
from pathlib import Path

# Ajouter le répertoire parent au PYTHONPATH
sys.path.append(str(Path(__file__).parent.parent))

from app.scrapers.allocine import AllocineScraper

def main():
    scraper = AllocineScraper()
    
    # Sauvegarder dans le dossier public de frontend
    output_path = Path(__file__).parent.parent.parent / 'frontend' / 'public' / 'seances.json'
    scraper.save_to_json(output_path)

if __name__ == "__main__":
    main() 