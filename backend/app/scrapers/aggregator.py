import json
from datetime import datetime
from typing import Dict, List
from .american_cosmograph import AmericanCosmographScraper
# Plus tard, nous importerons les autres scrapers ici

class SeanceAggregator:
    def __init__(self):
        self.scrapers = [
            AmericanCosmographScraper(),
            # Ajouter les autres scrapers ici
        ]

    def aggregate_seances(self) -> Dict:
        """Agrège toutes les séances de tous les cinémas"""
        all_seances = []
        for scraper in self.scrapers:
            all_seances.extend(scraper.get_seances())

        # Organiser par film
        films = {}
        for seance in all_seances:
            titre = seance['titre']
            if titre not in films:
                films[titre] = {
                    'seances_par_jour': {}
                }
            
            jour = seance['jour']
            if jour not in films[titre]['seances_par_jour']:
                films[titre]['seances_par_jour'][jour] = []
            
            films[titre]['seances_par_jour'][jour].append({
                'heure': seance['heure'],
                'cinema': seance['cinema']
            })

        return films

    def save_to_json(self, filename='all_seances.json'):
        films = self.aggregate_seances()
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(films, f, ensure_ascii=False, indent=2) 