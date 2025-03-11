import pytest
from app import create_app
from app.models import db
from app.models.cinema import Cinema
from backend.app.config import TestConfig
from app.models.film import Film
from app.models.seance import Seance
from datetime import datetime, timedelta, UTC

@pytest.fixture
def app():
    app = create_app(TestConfig)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def db_session(app):
    with app.app_context():
        db.create_all()
        yield db
        db.drop_all()

def test_create_cinema(db_session):
    cinema = Cinema(
        nom='American Cosmograph',
        adresse='24 Rue Montardy, 31000 Toulouse',
        site_web='https://www.american-cosmograph.fr'
    )
    db_session.session.add(cinema)
    db_session.session.commit()
    
    assert cinema.id is not None
    assert Cinema.query.count() == 1 

def test_create_film(db_session):
    film = Film(
        titre="Les Temps Modernes",
        realisateur="Charlie Chaplin",
        duree=87,
        annee=1936
    )
    db_session.session.add(film)
    db_session.session.commit()
    
    assert film.id is not None
    assert Film.query.count() == 1

def test_create_seance(db_session):
    # Créer un cinéma et un film
    cinema = Cinema(
        nom='American Cosmograph',
        adresse='24 Rue Montardy, 31000 Toulouse'
    )
    film = Film(
        titre="Les Temps Modernes",
        duree=87
    )
    
    # Créer une séance
    seance = Seance(
        date_heure=datetime.now(UTC) + timedelta(days=1),
        prix=7.50,
        langue="VO",
        film=film,
        cinema=cinema
    )
    
    db_session.session.add_all([cinema, film, seance])
    db_session.session.commit()
    
    assert seance.id is not None
    assert seance.film.titre == "Les Temps Modernes"
    assert seance.cinema.nom == "American Cosmograph" 

def test_film_seances_relationship(db_session):
    # Créer un film avec plusieurs séances dans différents cinémas
    film = Film(
        titre="Les Temps Modernes",
        duree=87
    )
    
    cinema1 = Cinema(nom='American Cosmograph')
    cinema2 = Cinema(nom='ABC')
    
    seance1 = Seance(
        date_heure=datetime.now(UTC) + timedelta(days=1),
        prix=7.50,
        film=film,
        cinema=cinema1
    )
    
    seance2 = Seance(
        date_heure=datetime.now(UTC) + timedelta(days=1, hours=2),
        prix=8.50,
        film=film,
        cinema=cinema2
    )
    
    db_session.session.add_all([film, cinema1, cinema2, seance1, seance2])
    db_session.session.commit()
    
    # Vérifier les relations
    assert film.seances.count() == 2
    assert cinema1.seances.count() == 1
    assert cinema2.seances.count() == 1
    assert seance1.film == film
    assert seance2.film == film

def test_cascade_delete(db_session):
    # Tester la suppression en cascade
    film = Film(titre="Film à supprimer")
    cinema = Cinema(nom='Cinéma test')
    seance = Seance(
        date_heure=datetime.now(UTC),
        film=film,
        cinema=cinema
    )
    
    db_session.session.add_all([film, cinema, seance])
    db_session.session.commit()
    
    # Supprimer le film devrait supprimer la séance
    db_session.session.delete(film)
    db_session.session.commit()
    
    assert Seance.query.count() == 0
    assert Cinema.query.count() == 1  # Le cinéma reste 