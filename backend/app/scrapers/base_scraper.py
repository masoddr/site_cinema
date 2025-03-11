from abc import ABC, abstractmethod
import json
from datetime import datetime
from typing import List, Dict

class BaseScraper(ABC):
    """Classe de base pour tous les scrapers de cinéma"""
    
    @abstractmethod
    def get_seances(self) -> List[Dict]:
        """Doit retourner une liste de séances"""
        pass

    def format_seance(self, titre: str, heure: str, jour: datetime, cinema: str) -> Dict:
        """Format standard pour une séance"""
        return {
            'titre': titre,
            'heure': heure,
            'jour': jour.strftime('%Y-%m-%d'),
            'cinema': cinema
        } 