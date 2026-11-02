import uuid
from datetime import datetime, timedelta, timezone
from functools import wraps

import bcrypt
import jwt
from flask import jsonify, request
from pymongo import MongoClient

from config.settings import settings

MEMORY_STORE = {
    'users': [],
    'simulation_results': [],
    'alerts': [],
    'quiz_results': [],
    'activity_logs': [],
}


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def get_db():
    if getattr(get_db, '_db', None) is not None:
        return get_db._db

    try:
        client = MongoClient(settings.MONGODB_URI, serverSelectionTimeoutMS=2000)
        client.admin.command('ping')
        db = client[settings.DB_NAME]
        get_db._db = db
        return db
    except Exception:
        get_db._db = None
        return None


def get_collection(name):
    db = get_db()
    if db is not None:
        return db[name]
    return MEMORY_STORE.setdefault(name, [])


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


def create_token(user_id, email):
    payload = {
        'user_id': str(user_id),
        'email': email,
        'exp': datetime.now(timezone.utc) + timedelta(days=7),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_token(token):
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])


def auth_required(view_func):
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        authorization = request.headers.get('Authorization', '')
        if not authorization.startswith('Bearer '):
            return jsonify({'error': 'Authentication token missing'}), 401

        token = authorization.split(' ', 1)[1].strip()
        try:
            payload = decode_token(token)
        except Exception:
            return jsonify({'error': 'Invalid or expired token'}), 401

        user = get_collection('users')
        if isinstance(user, list):
            current_user = next((doc for doc in user if str(doc.get('_id')) == str(payload.get('user_id'))), None)
        else:
            current_user = user.find_one({'_id': payload.get('user_id')})

        if current_user is None:
            return jsonify({'error': 'User not found'}), 401

        return view_func(current_user, *args, **kwargs)

    return wrapped


def generate_id():
    return str(uuid.uuid4())
