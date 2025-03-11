from flask import jsonify
from app.models.cinema import Cinema
from app.routes import api

@api.route('/cinemas', methods=['GET'])
def get_cinemas():
    cinemas = Cinema.query.all()
    return jsonify([cinema.to_dict() for cinema in cinemas])

@api.route('/cinema/<int:id>', methods=['GET'])
def get_cinema(id):
    cinema = Cinema.query.get_or_404(id)
    return jsonify(cinema.to_dict()) 