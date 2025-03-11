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

## Installation et test en local

### Prérequis
- Python 3.8 ou supérieur
- pip
- virtualenv (recommandé)

### Installation

1. Créer et activer un environnement virtuel :
```bash
python -m venv venv
source venv/bin/activate  # Sur Linux/MacOS
# ou
venv\Scripts\activate  # Sur Windows
```

2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

### Lancer l'application en local

1. Configurer les variables d'environnement :
```bash
export FLASK_APP=app
export FLASK_ENV=development
```

2. Lancer le serveur backend :
```bash
# Depuis le dossier backend/
flask run
```

Le serveur backend sera accessible à l'adresse : http://localhost:5000

3. Lancer le frontend (dans un nouveau terminal) :
```bash
# Depuis le dossier frontend/
npm install  # Uniquement la première fois pour installer les dépendances
npm run dev
```

Le frontend sera accessible à l'adresse : http://localhost:3000

### Architecture en développement

En développement, l'application fonctionne avec :
- Le backend Flask sur le port 5000
- Le frontend React sur le port 3000
- Une configuration CORS permettant la communication entre les deux serveurs

Pour vérifier que tout fonctionne :
1. Ouvrez http://localhost:3000 dans votre navigateur
2. Vérifiez que le frontend arrive à communiquer avec le backend en consultant les séances de cinéma
3. Vous pouvez aussi tester l'API directement via http://localhost:5000/api/seances

### Tester les scrapers individuellement

Vous pouvez tester chaque scraper séparément en exécutant les scripts correspondants :

```bash
python scripts/scrape_abc.py
# ou
python scripts/scrape_american_cosmograph.py
```

Les résultats seront sauvegardés dans les fichiers JSON correspondants dans le dossier courant. 