# CinéToulouse - Agrégateur de Programmation Cinéma

## 📝 Description du Projet
Application web permettant de consulter en un seul endroit la programmation des cinémas de Toulouse :
- American Cosmograph
- ABC
- Pathé Wilson

On utiliseras une méthode TDD pour développer le projet.
On mettra à jour les parties docker tout au long du projet pour tester les différentes fonctionnalités.
Tu mettras à jour ce document tout au long du projet.

## 🏗 Architecture Technique

### Stack Technique
- **Backend** : Python/Flask
- **Frontend** : Astro 
- **Base de données** : PostgreSQL
- **Scraping** : BeautifulSoup4/Scrapy

### Structure du Projet
site_cinema/
├── backend/
│ ├── app/
│ │ ├── __init__.py
│ │ ├── models/
│ │ ├── routes/
│ │ └── scrapers/
│ ├── tests/
│ ├── requirements.txt
│ └── config.py
├── frontend/
│ ├── src/
│ ├── public/
│ └── astro.config.mjs
├── database/
│ └── schema.sql
├── docker/
│ ├── frontend/
│ │ ├── Dockerfile
│ │ └── Dockerfile.dev
│ ├── backend/
│ │ ├── Dockerfile
│ │ └── Dockerfile.dev
│ └── scraper/
│     └── Dockerfile
├── docker-compose.yml
├── docker-compose.dev.yml
├── Makefile
├── README.md
├── .env.example
├── devbook.md
└── .gitignore

## 📊 Structure de la Base de Données

### Tables Principales
- `cinemas` : Informations sur les cinémas
- `films` : Détails des films
- `seances` : Horaires des séances

## 🔄 Flux de Données
1. Scraping quotidien des sites web des cinémas
2. Mise à jour de la base de données
3. Exposition via API REST
4. Affichage sur le frontend

## 📋 Fonctionnalités Principales
- [ ] Consultation des films par cinéma
- [ ] Filtrage par date
- [ ] Recherche de films
- [ ] Affichage des détails des séances (langue, sous-titres)
- [ ] Vue calendrier hebdomadaire

## 🛠 Configuration du Développement

### Prérequis
- Python 3.8+
- Node.js 16+
- PostgreSQL 13+

### Installation

Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
Frontend

## 📅 Phases de Développement

### Phase 1 : Mise en place du Scraping
- [ ] Développement du scraper American Cosmograph
- [ ] Développement du scraper ABC
- [ ] Développement du scraper Pathé Wilson
- [ ] Tests unitaires des scrapers
- [ ] Système de logging

### Phase 2 : Backend et Base de Données
- [x] Création du schéma de base de données
- [ ] Mise en place de l'API Flask
- [ ] Endpoints CRUD
- [ ] Documentation API
- [ ] Tests d'intégration

### Phase 3 : Frontend
- [ ] Setup du projet Astro
- [ ] Création des composants UI
- [ ] Intégration avec l'API
- [ ] Tests E2E

### Phase 4 : Déploiement
- [ ] Configuration serveur de production
- [ ] Mise en place CI/CD
- [ ] Monitoring
- [ ] Backup automatique

## 🔒 Variables d'Environnement

DATABASE_URL=postgresql://user:password@localhost:5432/cinema_toulouse
FLASK_ENV=development
SCRAPING_INTERVAL=24 # en heures

## 📚 Documentation Utile
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Astro Documentation](https://docs.astro.build/)
- [Beautiful Soup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

## 🤝 Contribution
Instructions pour contribuer au projet...

## 📝 Notes
- Vérifier les conditions d'utilisation des sites web des cinémas
- Prévoir une mise à jour quotidienne des données
- Gérer les cas d'erreur lors du scraping

## 📱 Maquettes & Pages

### Page d'Accueil
- Header avec logo et navigation
- Barre de recherche principale
- Filtres rapides (cinéma, date, langue)
- Vue "Aujourd'hui" par défaut avec :
  - Films à l'affiche
  - Pour chaque film :
    * Affiche
    * Titre
    * Durée
    * Langues/Sous-titres disponibles
    * Liste des séances par cinéma
    * Quick-actions (voir détails, réserver)

### Vue Hebdomadaire (/semaine)
- Calendrier horizontal (7 jours)
- Liste des films groupés par jour
- Pour chaque film :
  * Miniature affiche
  * Titre et infos essentielles
  * Séances du jour par cinéma
  * Code couleur par cinéma

### Page Film (/film/[id])
- Affiche grand format
- Informations détaillées
  * Synopsis
  * Durée
  * Réalisateur
  * Genre
  * Année
- Toutes les séances à venir
- Lien vers les sites de réservation des cinémas

### Composants UI Principaux
- FilmCard : carte film réutilisable
- SeancesList : liste des séances par cinéma
- DatePicker : sélecteur de date personnalisé
- CinemaFilter : filtres multi-cinémas
- SearchBar : recherche avec autocomplétion

### Navigation
- Accueil (vue du jour)
- Planning hebdomadaire
- Par cinéma
- Recherche
- À propos

## 🎨 Design System
- Palette de couleurs :
  * Principal : #2C3E50 (bleu nuit)
  * Secondaire : #E74C3C (rouge ciné)
  * Accent : #F1C40F (jaune)
  * Fond : #F8F9FA
- Typography :
  * Titres : Montserrat
  * Corps : Open Sans
- Composants cohérents avec états hover/focus
- Design responsive mobile-first

## 🐳 Docker & Développement

### Structure Docker

site_cinema/
├── docker/
│ ├── frontend/
│ │ ├── Dockerfile
│ │ └── Dockerfile.dev
│ ├── backend/
│ │ ├── Dockerfile
│ │ └── Dockerfile.dev
│ └── scraper/
│ └── Dockerfile
├── docker-compose.yml
├── docker-compose.dev.yml
├── README.md
├── .env.example
├── devbook.md
└── .gitignore

### Configuration Docker
- `docker-compose.yml` : Configuration de production
- `docker-compose.dev.yml` : Configuration de développement avec :
  * Volumes montés pour hot-reload
  * Ports exposés pour debugging
  * Variables d'environnement de développement
  * Outils de développement supplémentaires


