from flask import jsonify
from app.models.cinema import Cinema
from . import main

@main.route('/cinemas')
def get_cinemas():
    cinemas = Cinema.query.all()
    return jsonify([{
        'id': c.id,
        'nom': c.nom,
        'adresse': c.adresse,
        'site_web': c.site_web
    } for c in cinemas]) 