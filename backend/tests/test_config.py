import pytest
from app import create_app
from backend.app.config import Config

def test_config():
    app = create_app()
    assert app.config['SCRAPING_INTERVAL'] == 24
    assert 'postgresql://' in app.config['SQLALCHEMY_DATABASE_URI']
    
def test_health_endpoint():
    app = create_app()
    client = app.test_client()
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json == {'status': 'ok'} 