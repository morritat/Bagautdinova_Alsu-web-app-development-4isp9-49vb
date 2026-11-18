"""Защита от CSRF-атак через токены."""
import secrets
from functools import wraps
from flask import session, request, jsonify


def generate_csrf_token() -> str:
    """Генерирует и сохраняет CSRF-токен в сессии."""
    if '_csrf_token' not in session:
        session['_csrf_token'] = secrets.token_hex(32)
    return session['_csrf_token']


def csrf_protect(f):
    """Декоратор CSRF-защиты для POST/PUT/DELETE запросов."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.method in ('POST', 'PUT', 'DELETE'):
            token = request.headers.get('X-CSRF-Token') or \
                    request.form.get('csrf_token')
            if not token or token != session.get('_csrf_token'):
                return jsonify({
                    'success': False,
                    'message': 'CSRF-токен отсутствует или некорректен'
                }), 403
        return f(*args, **kwargs)
    return decorated