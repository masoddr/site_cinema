import json
import requests
from typing import Dict, Optional
import time
from datetime import datetime
import os
from pathlib import Path

# Obtenir le chemin absolu du répertoire racine du projet
PROJECT_ROOT = Path(__file__).parent.parent.parent
SEANCES_FILE = PROJECT_ROOT / "frontend" / "public" / "seances.json"
CACHE_FILE = PROJECT_ROOT / "backend" / "data" / "tmdb_cache.json"
SEANCES_CACHE_FILE = PROJECT_ROOT / "backend" / "data" / "seances_cache.json"

TMDB_API_KEY = "21698af2bd148f0cfedc858588259fa0"
TMDB_BASE_URL = "https://api.themoviedb.org/3"

def search_movie_tmdb(title: str, is_french_version: bool = False) -> Optional[Dict]:
    """
    Recherche un film sur TMDb et retourne les détails pertinents
    """
    try:
        # Paramètres de recherche
        params = {
            "api_key": TMDB_API_KEY,
            "query": title,
            "language": "fr-FR",
            "region": "FR"
        }
        
        # Recherche du film
        search_response = requests.get(
            f"{TMDB_BASE_URL}/search/movie",
            params=params
        )
        search_response.raise_for_status()
        results = search_response.json().get("results", [])
        
        if not results:
            return None
            
        # Prendre le premier résultat
        movie_id = results[0]["id"]
        
        # Obtenir les détails complets du film
        details_response = requests.get(
            f"{TMDB_BASE_URL}/movie/{movie_id}",
            params={"api_key": TMDB_API_KEY, "language": "fr-FR"}
        )
        details_response.raise_for_status()
        movie_details = details_response.json()
        
        # Obtenir la bande-annonce
        trailer_url = get_movie_trailer(movie_id)
        
        return {
            "tmdb_id": movie_id,
            "runtime": movie_details.get("runtime"),
            "release_date": movie_details.get("release_date"),
            "vote_average": movie_details.get("vote_average"),
            "trailer_url": trailer_url
        }
        
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la recherche de {title}: {str(e)}")
        return None

def load_cache() -> Dict:
    """
    Charge le cache TMDb depuis le fichier
    """
    if CACHE_FILE.exists():
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"last_updated": datetime.now().isoformat(), "movies": {}}

def save_cache(cache: Dict):
    """
    Sauvegarde le cache TMDb dans le fichier
    """
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

def update_seances_with_tmdb_data():
    """
    Met à jour les fichiers seances.json et seances_cache.json avec les données TMDb
    """
    # Charger les séances existantes
    with open(SEANCES_FILE, "r", encoding="utf-8") as f:
        seances = json.load(f)
    
    # Charger le cache TMDb
    cache = load_cache()
    tmdb_cache = cache["movies"]
    
    # Liste pour stocker les séances mises à jour
    updated_seances = []
    
    # Mettre à jour chaque séance
    for seance in seances:
        titre = seance["titre"]
        is_french = seance["version"] == "VF"
        
        # Utiliser le cache si disponible
        if titre not in tmdb_cache:
            print(f"Recherche des données TMDb pour: {titre}")
            tmdb_data = search_movie_tmdb(titre, is_french)
            if tmdb_data:
                tmdb_cache[titre] = tmdb_data
            time.sleep(0.25)  # Respecter les limites de l'API
        
        # Créer une copie de la séance pour la mise à jour
        updated_seance = seance.copy()
        
        # Mettre à jour la séance avec les données TMDb
        if titre in tmdb_cache:
            data = tmdb_cache[titre]
            updated_seance["duree"] = data["runtime"]
            updated_seance["tmdb_id"] = data["tmdb_id"]
            updated_seance["date_sortie"] = data["release_date"]
            updated_seance["note"] = data["vote_average"]
            updated_seance["trailer_url"] = data.get("trailer_url")
        
        updated_seances.append(updated_seance)
    
    # Sauvegarder le cache TMDb mis à jour
    cache["last_updated"] = datetime.now().isoformat()
    save_cache(cache)
    
    # Sauvegarder les séances mises à jour dans seances.json
    with open(SEANCES_FILE, "w", encoding="utf-8") as f:
        json.dump(updated_seances, f, ensure_ascii=False, indent=2)
    
    # Créer la structure du cache des séances
    seances_cache_data = {
        "last_update": datetime.now().isoformat(),
        "seances": updated_seances
    }
    
    # Sauvegarder dans seances_cache.json
    with open(SEANCES_CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(seances_cache_data, f, ensure_ascii=False, indent=2)
    
    print("Mise à jour terminée!")

def get_movie_trailer(tmdb_id):
    response = requests.get(
        f"{TMDB_BASE_URL}/movie/{tmdb_id}/videos",
        params={
            "api_key": TMDB_API_KEY,
            "language": "fr-FR"
        }
    )
    
    if response.status_code != 200:
        return None
        
    videos = response.json()["results"]
    
    # Chercher d'abord une bande-annonce officielle en français
    for video in videos:
        if video["site"] == "YouTube" and video["type"] == "Trailer" and video["iso_639_1"] == "fr":
            return f"https://www.youtube.com/watch?v={video['key']}"
    
    # Sinon, prendre la première bande-annonce disponible
    for video in videos:
        if video["site"] == "YouTube" and video["type"] == "Trailer":
            return f"https://www.youtube.com/watch?v={video['key']}"
            
    return None

def get_movie_data(tmdb_id):
    # ... existing code ...
    
    movie_data = {
        # ... autres données existantes ...
        "trailer_url": get_movie_trailer(tmdb_id)
    }
    
    return movie_data

if __name__ == "__main__":
    update_seances_with_tmdb_data() 