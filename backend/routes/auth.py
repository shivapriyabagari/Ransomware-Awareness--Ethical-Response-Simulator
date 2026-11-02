from flask import Blueprint, jsonify, request

from models.user import public_user
from utils.helpers import (
    auth_required,
    create_token,
    generate_id,
    get_collection,
    hash_password,
    verify_password,
)

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/api/auth/register', methods=['POST'])
def register():
    payload = request.get_json(silent=True) or {}
    name = (payload.get('name') or '').strip()
    email = (payload.get('email') or '').strip().lower()
    password = (payload.get('password') or '').strip()

    if not name or not email or not password:
        return jsonify({'error': 'Name, email, and password are required'}), 400

    users = get_collection('users')
    exists = None
    if hasattr(users, 'find_one'):
        exists = users.find_one({'email': email})
    else:
        exists = next((user for user in users if user.get('email') == email), None)

    if exists:
        return jsonify({'error': 'User already exists'}), 409

    user_doc = {
        '_id': generate_id(),
        'name': name,
        'email': email,
        'password_hash': hash_password(password),
        'created_at': __import__('datetime').datetime.utcnow().isoformat() + 'Z',
    }

    if hasattr(users, 'insert_one'):
        users.insert_one(user_doc)
    else:
        users.append(user_doc)

    token = create_token(user_doc['_id'], email)
    return jsonify({'token': token, 'user': public_user(user_doc)}), 201


@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    payload = request.get_json(silent=True) or {}
    email = (payload.get('email') or '').strip().lower()
    password = (payload.get('password') or '').strip()

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    users = get_collection('users')
    user = None
    if hasattr(users, 'find_one'):
        user = users.find_one({'email': email})
    else:
        user = next((item for item in users if item.get('email') == email), None)

    if user is None:
        return jsonify({'error': 'Invalid credentials'}), 401

    stored_hash = user.get('password_hash') or ''
    if not verify_password(password, stored_hash):
        return jsonify({'error': 'Invalid credentials'}), 401

    token = create_token(user['_id'], email)
    return jsonify({'token': token, 'user': public_user(user)})


@auth_bp.route('/api/auth/me', methods=['GET'])
@auth_required
def current_user(user):
    return jsonify({'user': public_user(user)})


@auth_bp.route('/api/auth/logout', methods=['POST'])
def logout():
    return jsonify({'message': 'Logged out successfully'})
