import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from allocineAPI.allocineAPI import allocineAPI
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_cinema_ids():
    api = allocineAPI()
    
    # Récupérer les cinémas de Toulouse
    logger.info("Recherche des cinémas à Toulouse...")
    
    # D'abord trouver l'ID de Toulouse
    villes = api.get_top_villes()
    toulouse_id = None
    for ville in villes:
        if "Toulouse" in ville['name']:
            toulouse_id = ville['id']
            break
    
    if not toulouse_id:
        logger.error("❌ Impossible de trouver l'ID de Toulouse")
        return
        
    logger.info(f"ID de Toulouse trouvé : {toulouse_id}")
    
    # Récupérer tous les cinémas de Toulouse
    cinemas = api.get_cinema(toulouse_id)
    logger.info("\nCinémas trouvés à Toulouse :")
    for cinema in cinemas:
        logger.info(f"- {cinema['name']} (ID: {cinema['id']})")
        if "ABC" in cinema['name'] or "Cosmograph" in cinema['name']:
            logger.info(f"  ⭐ TROUVÉ : {cinema['name']} - {cinema['id']}")

if __name__ == "__main__":
    test_cinema_ids() 