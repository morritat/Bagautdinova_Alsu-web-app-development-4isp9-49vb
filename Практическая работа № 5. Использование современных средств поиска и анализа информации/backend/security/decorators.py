"""Декораторы разграничения прав доступа."""
from functools import wraps
from flask import session, jsonify, redirect, url_for, request


def login_required(f):
    """Требует авторизации. Иначе — 401 или редирект на /login."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            if request.is_json:
                return jsonify({
                    'success': False,
                    'message': 'Требуется авторизация'
                }), 401
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    """Требует роли admin."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            if request.is_json:
                return jsonify({
                    'success': False,
                    'message': 'Требуется авторизация'
                }), 401
            return redirect(url_for('auth.login'))
        if session.get('role') != 'admin':
            if request.is_json:
                return jsonify({
                    'success': False,
                    'message': 'Доступ запрещён. Требуются права администратора.'
                }), 403
            return jsonify({'error': 'Forbidden'}), 403
        return f(*args, **kwargs)
    return decorated


def check_role(*roles):
    """Декоратор для проверки роли пользователя."""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if session.get('role') not in roles:
                return jsonify({
                    'success': False,
                    'message': 'Недостаточно прав'
                }), 403
            return f(*args, **kwargs)
        return decorated
    return decorator