def public_user(user):
    if not user:
        return None
    user_payload = dict(user)
    user_payload.pop('password_hash', None)
    user_payload.pop('password', None)
    if '_id' in user_payload:
        user_payload['id'] = str(user_payload['_id'])
        user_payload.pop('_id')
    return user_payload
