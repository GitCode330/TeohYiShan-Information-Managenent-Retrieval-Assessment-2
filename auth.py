import requests
from flask import request, jsonify
from functools import wraps

AUTH_API_URL = "https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users"

# For testing, accept these dummy tokens
TEST_TOKENS = {
    'test_token_101': {'id': 101, 'name': 'Ada Lovelace'},
    'test_token_102': {'id': 102, 'name': 'Tim Berners-Lee'},
    'test_token_103': {'id': 103, 'name': 'Grace Hopper'},
    'dummy_token_cw2': {'id': 101, 'name': 'Test User'}
}

def validate_token(token):
    """Validate token with external Authenticator API"""
    # First check if it's a test token
    if token in TEST_TOKENS:
        return True
    
    # If not test token, try real API (for final deployment)
    try:
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(f"{AUTH_API_URL}/validate", headers=headers, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

def get_user_from_token(token):
    """Get user information from token"""
    # Return test user data for test tokens
    if token in TEST_TOKENS:
        return TEST_TOKENS[token]

    # For real tokens, call API
    try:
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(AUTH_API_URL, headers=headers, timeout=5)
        if response.status_code == 200:
            return response.json()
        return None
    except requests.RequestException:
        return None

def token_required(f):
    """Decorator to require valid JWT token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Get token from header
        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            token = auth_header.split(" ")[1]
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        if not validate_token(token):
            return jsonify({'message': 'Token is invalid!'}), 401
        
        # Store user info in request context
        user_data = get_user_from_token(token)
        if user_data:
            request.user_data = user_data
        
        return f(*args, **kwargs)
    
    return decorated

def owner_required(f):
    """Decorator to check if user owns the trail"""
    @wraps(f)
    def decorated(trail_id, *args, **kwargs):
        from models import Trail
        
        trail = Trail.query.filter_by(TrailID=trail_id).first()
        if not trail:
            return jsonify({'message': 'Trail not found!'}), 404
        
        # Get user from token (simplified - in real implementation, decode JWT)
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user_data = get_user_from_token(token)
        
        if not user_data or user_data.get('id') != trail.OwnerUserID:
            return jsonify({'message': 'You are not the owner of this trail!'}), 403
        
        return f(trail_id, *args, **kwargs)
    
    return decorated