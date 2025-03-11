# Guide de développement

## Structure du projet 
```
+ backend/
+ ├── app/
+ │   ├── scrapers/
+ │   │   ├── __init__.py
+ │   │   ├── base_scraper.py
+ │   │   ├── american_cosmograph.py
+ │   │   └── abc.py
+ │   └── models/
+ │       ├── __init__.py
+ │       └── film.py
+ ├── scripts/
+ │   ├── scrape_abc.py
+ │   ├── scrape_american_cosmograph.py
+ │   └── scrape_all.py
+ └── tests/
+     ├── test_config.py
+     └── test_models.py
+ ```

## Scrapers

### Fonctionnement général

Les scrapers récupèrent les séances de cinéma depuis les sites web. Chaque scraper hérite de `BaseScraper` et implémente sa propre logique de scraping.

### Format des données

Les séances sont sauvegardées au format JSON avec la structure suivante :
```json
{
    "titre": "Nom du film",
    "heure": "14h30",
    "jour": "2025-03-11T00:00:00",
    "cinema": "Nom du cinéma",
    "salle": "1",
    "duree": "1h30",
    "version": "VF/VOST",
    "tags": []
}
```

### Spécificités des cinémas

#### American Cosmograph
- Affiche toute la semaine directement
- Les salles sont numérotées (1, 2, 3)
- URL : https://www.american-cosmograph.fr/les-horaires.html

#### ABC
- Affiche les séances du mercredi au mardi
- Les salles sont nommées par lettres (a, b, c)
- URL : https://abc-toulouse.fr/horaires.html
- **Important** : La programmation change le mercredi, il faut donc scraper ce jour-là pour avoir la semaine complète

### Cronjob

Pour maintenir les données à jour, un cronjob doit être configuré pour s'exécuter tous les mercredis :

```bash
# Exécuter le scraping tous les mercredis à 1h du matin
0 1 * * 3 cd /path/to/project && /path/to/venv/bin/python scripts/scrape_all.py
```

### Scripts disponibles

- `scrape_all.py` : Lance le scraping pour tous les cinémas
- `scrape_abc.py` : Lance uniquement le scraping de l'ABC
- `scrape_american_cosmograph.py` : Lance uniquement le scraping de l'American Cosmograph

### Fichiers de sortie

- `american_cosmograph_seances.json` : Séances de l'American Cosmograph
- `abc_seances.json` : Séances de l'ABC
- `debug_abc.html` : Fichier de debug pour l'ABC (HTML brut)

## Tests

Les tests sont dans le dossier `tests/` et peuvent être lancés avec pytest. 