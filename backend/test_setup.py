def test_import_dependencies():
    # Test des imports principaux
    import flask
    import flask_cors
    import psycopg2
    import sqlalchemy
    import bs4
    import requests
    import scrapy
    import pytest
    import dotenv
    
    assert True, "Tous les imports fonctionnent correctement"

def test_flask_version():
    import flask
    assert flask.__version__ == "3.0.2", "Version de Flask correcte" 