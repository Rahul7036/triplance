from flask import Blueprint, request, jsonify
from app.models.trip import Trip
from app import db
from datetime import datetime
from app.auth.routes import token_required

trips_bp = Blueprint('trips', __name__)

@trips_bp.route('/trips', methods=['POST'])
@token_required
def create_trip(current_user):
    data = request.get_json()
    
    try:
        new_trip = Trip(
            title=data['title'],
            destination=data['destination'],
            start_date=datetime.strptime(data['start_date'], '%Y-%m-%d').date(),
            end_date=datetime.strptime(data['end_date'], '%Y-%m-%d').date(),
            description=data.get('description', ''),
            user_id=current_user.id
        )
        
        db.session.add(new_trip)
        db.session.commit()
        
        return jsonify(new_trip.to_dict()), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@trips_bp.route('/trips', methods=['GET'])
@token_required
def get_trips(current_user):
    trips = Trip.query.filter_by(user_id=current_user.id).all()
    return jsonify([trip.to_dict() for trip in trips]), 200

@trips_bp.route('/trips/<int:trip_id>', methods=['GET'])
@token_required
def get_trip(current_user, trip_id):
    trip = Trip.query.filter_by(id=trip_id, user_id=current_user.id).first()
    if not trip:
        return jsonify({'error': 'Trip not found'}), 404
    return jsonify(trip.to_dict()), 200

@trips_bp.route('/trips/<int:trip_id>', methods=['PUT'])
@token_required
def update_trip(current_user, trip_id):
    trip = Trip.query.filter_by(id=trip_id, user_id=current_user.id).first()
    if not trip:
        return jsonify({'error': 'Trip not found'}), 404
    
    data = request.get_json()
    
    try:
        if 'title' in data:
            trip.title = data['title']
        if 'destination' in data:
            trip.destination = data['destination']
        if 'start_date' in data:
            trip.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        if 'end_date' in data:
            trip.end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
        if 'description' in data:
            trip.description = data['description']
            
        db.session.commit()
        return jsonify(trip.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@trips_bp.route('/trips/<int:trip_id>', methods=['DELETE'])
@token_required
def delete_trip(current_user, trip_id):
    trip = Trip.query.filter_by(id=trip_id, user_id=current_user.id).first()
    if not trip:
        return jsonify({'error': 'Trip not found'}), 404
    
    db.session.delete(trip)
    db.session.commit()
    return jsonify({'message': 'Trip deleted successfully'}), 200