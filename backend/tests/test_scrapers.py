import pytest
from datetime import datetime
from app.scrapers.american_cosmograph import AmericanCosmographScraper

def test_american_cosmograph_scraper():
    scraper = AmericanCosmographScraper()
    seances = scraper.get_seances()
    
    # Vérifier la structure des données
    assert len(seances) > 0
    for seance in seances:
        assert isinstance(seance, dict)
        assert all(key in seance for key in ['titre', 'heure', 'jour', 'cinema'])
        assert seance['cinema'] == 'American Cosmograph'
        # Vérifier le format de l'heure (HH:MM)
        assert len(seance['heure'].split(':')) == 2
        # Vérifier que le jour est une date valide
        assert isinstance(seance['jour'], datetime) 