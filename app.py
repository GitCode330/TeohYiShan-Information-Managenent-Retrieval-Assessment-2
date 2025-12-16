from flask import Flask, request, jsonify
from flask_cors import CORS
from database import db, init_db
from models import User, Trail, Feature, TrailAuditLog
from auth import token_required, owner_required
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize database
init_db(app)

# Test endpoint
@app.route('/')
def home():
    return jsonify({
        'message': 'TrailService API',
        'version': '1.0',
        'endpoints': {
            'GET /trails': 'Get all trails',
            'GET /trails/<id>': 'Get specific trail',
            'POST /trails': 'Create new trail (requires auth)',
            'PUT /trails/<id>': 'Update trail (requires owner)',
            'DELETE /trails/<id>': 'Delete trail (requires owner)',
            'GET /features': 'Get all features'
        }
    })

# Get all trails
@app.route('/trails', methods=['GET'])
def get_trails():
    try:
        trails = Trail.query.all()
        result = []
        for trail in trails:
            result.append({
                'trail_id': trail.TrailID,  
                'trail_name': trail.TrailName,  
                'description': trail.Description,  
                'difficulty': trail.Difficulty, 
                'length': float(trail.Length), 
                'elevation_gain': trail.ElevationGain, 
                'owner_user_id': trail.OwnerUserID,  
                'features': [] 
            })
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get specific trail
@app.route('/trails/<int:trail_id>', methods=['GET'])
def get_trail(trail_id):
    try:
        trail = Trail.query.filter_by(TrailID=trail_id).first()
        if not trail:
            return jsonify({'message': 'Trail not found'}), 404
        
        result = {
            'trail_id': trail.TrailID,  
            'trail_name': trail.TrailName,  
            'description': trail.Description,  
            'difficulty': trail.Difficulty, 
            'length': float(trail.Length),  
            'elevation_gain': trail.ElevationGain,  
            'owner_user_id': trail.OwnerUserID,  
            'features': []  
        }
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Create new trail (requires authentication)
@app.route('/trails', methods=['POST'])
@token_required
def create_trail():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['trail_name', 'difficulty', 'length', 'elevation_gain', 'owner_user_id']
        for field in required_fields:
            if field not in data:
                return jsonify({'message': f'{field} is required'}), 400
        
        # Validate difficulty
        if data['difficulty'] not in ['Easy', 'Moderate', 'Hard']:
            return jsonify({'message': 'Difficulty must be Easy, Moderate, or Hard'}), 400
        
        # Validate numeric values
        if data['length'] <= 0:
            return jsonify({'message': 'Length must be positive'}), 400
        if data['elevation_gain'] < 0:
            return jsonify({'message': 'Elevation gain cannot be negative'}), 400
        
        # Create new trail
        new_trail = Trail(
            TrailName=data['trail_name'],  
            Description=data.get('description', ''),  
            Difficulty=data['difficulty'],  
            Length=data['length'],  
            ElevationGain=data['elevation_gain'], 
            OwnerUserID=data['owner_user_id']  
        )
        
        db.session.add(new_trail)
        db.session.commit()
        
        # Add features if provided
        if 'feature_ids' in data:
            for feature_id in data['feature_ids']:
                # Check if feature exists
                feature = Feature.query.filter_by(feature_id=feature_id).first()
                if feature:
                    new_trail.features.append(feature)
            
            db.session.commit()
        
        # Manually log to audit table (trigger would do this automatically)
        audit_log = TrailAuditLog(
            TrailID=new_trail.TrailID,  
            TrailName=new_trail.TrailName, 
            AddedByUserID=new_trail.OwnerUserID
        )
        db.session.add(audit_log)
        db.session.commit()
        
        return jsonify({
            'message': 'Trail created successfully',
            'trail_id': new_trail.TrailID
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Update trail (requires owner authentication)
@app.route('/trails/<int:trail_id>', methods=['PUT'])
@token_required
@owner_required
def update_trail(trail_id):
    try:
        trail = Trail.query.filter_by(TrailID=trail_id).first()
        if not trail:
            return jsonify({'message': 'Trail not found'}), 404
        
        data = request.get_json()
        
        # Update fields if provided
        if 'trail_name' in data:
            trail.TrailName = data['trail_name']  
        if 'description' in data:
            trail.Description = data['description']  
        if 'difficulty' in data:
            if data['difficulty'] not in ['Easy', 'Moderate', 'Hard']:
                return jsonify({'message': 'Difficulty must be Easy, Moderate, or Hard'}), 400
            trail.Difficulty = data['difficulty']  
        if 'length' in data:
            if data['length'] <= 0:
                return jsonify({'message': 'Length must be positive'}), 400
            trail.Length = data['length']  
        if 'elevation_gain' in data:
            if data['elevation_gain'] < 0:
                return jsonify({'message': 'Elevation gain cannot be negative'}), 400
            trail.ElevationGain = data['elevation_gain']
        
        # Update features if provided
        if 'feature_ids' in data:
            trail.features = []
            for feature_id in data['feature_ids']:
                feature = Feature.query.filter_by(feature_id=feature_id).first()
                if feature:
                    trail.features.append(feature)
        
        db.session.commit()
        
        return jsonify({'message': 'Trail updated successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Delete trail (requires owner authentication)
@app.route('/trails/<int:trail_id>', methods=['DELETE'])
@token_required
@owner_required
def delete_trail(trail_id):
    try:
        trail = Trail.query.filter_by(TrailID=trail_id).first()
        if not trail:
            return jsonify({'message': 'Trail not found'}), 404
        
        db.session.delete(trail)
        db.session.commit()
        
        return jsonify({'message': 'Trail deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Get all features
@app.route('/features', methods=['GET'])
def get_features():
    try:
        features = Feature.query.all()
        result = [{'feature_id': f.FeatureID, 'feature_name': f.FeatureName} for f in features]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get audit logs (for testing/verification)
@app.route('/audit-logs', methods=['GET'])
@token_required
def get_audit_logs():
    try:
        logs = TrailAuditLog.query.order_by(TrailAuditLog.DateAdded.desc()).limit(10).all()
        result = []
        for log in logs:
            result.append({
                'log_id': log.LogID,  
                'trail_id': log.TrailID,  
                'trail_name': log.TrailName,  
                'added_by_user_id': log.AddedByUserID,  
                'date_added': log.DateAdded.isoformat() if log.DateAdded else None
            })
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Test endpoint to get test tokens
@app.route('/test-tokens', methods=['GET'])
def get_test_tokens():
    """Return test tokens for development"""
    return jsonify({
        'test_tokens': [
            {'token': 'test_token_101', 'user_id': 101, 'user_name': 'Ada Lovelace', 'owns_trails': [1]},
            {'token': 'test_token_102', 'user_id': 102, 'user_name': 'Tim Berners-Lee', 'owns_trails': [2]},
            {'token': 'test_token_103', 'user_id': 103, 'user_name': 'Grace Hopper', 'owns_trails': [3]},
            {'token': 'dummy_token_cw2', 'user_id': 101, 'user_name': 'Test User'}
        ],
        'instructions': 'Use in Authorization header: Bearer <token>'
    }), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)