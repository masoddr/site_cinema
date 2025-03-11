import requests
from app.constants.cinemas import CINEMAS

def test_cinema_ids():
    for cinema_code, info in CINEMAS.items():
        cinema_id = info['id']
        
        # Test de l'URL du site web
        web_url = f"https://www.allocine.fr/seance/salle_gen_csalle={cinema_id}.html"
        web_response = requests.get(web_url)
        
        # Test de l'URL de l'API
        api_url = f"https://www.allocine.fr/_/showtimes/theater-{cinema_id}/2024-03-05"
        api_response = requests.get(api_url)
        
        print(f"\nTest pour {info['name']} (ID: {cinema_id}):")
        print(f"URL Web: {'✅ OK' if web_response.status_code == 200 else '❌ ERREUR'}")
        print(f"URL API: {'✅ OK' if api_response.status_code == 200 and api_response.json() else '❌ ERREUR'}")

if __name__ == "__main__":
    test_cinema_ids() 