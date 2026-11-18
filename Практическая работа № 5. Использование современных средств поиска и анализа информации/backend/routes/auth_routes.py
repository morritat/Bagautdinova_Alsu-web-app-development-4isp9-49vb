from flask import Blueprint, request, jsonify, render_template, session
from backend.models.user import User
from backend.security.rate_limiter import rate_limit, login_limiter
from backend.security.sanitizer import sanitize_dict
from backend.security.audit_log import log_action

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    data = sanitize_dict(request.get_json() or {})
    user = User(
        login=data.get('login', '').strip(),
        password=data.get('password', ''),
        email=data.get('email', '').strip(),
        phone=data.get('phone', '').strip(),
        role='user'
    )
    ok, result = user.save()
    
    if not ok:
        log_action('register_failed', {'login': data.get('login'), 'error': result})
        return jsonify({'success': False, 'message': result}), 400
    
    log_action('register_success', {'user_id': result})
    return jsonify({'success': True, 'user_id': result}), 201


@auth_bp.route('/login', methods=['GET', 'POST'])
@rate_limit(login_limiter)  # ← ЗАЩИТА ОТ БРУТФОРСА
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    data = sanitize_dict(request.get_json() or {})
    user = User.authenticate(
        data.get('login', ''),
        data.get('password', '')
    )
    
    if not user:
        log_action('login_failed', {'login': data.get('login')})
        return jsonify({
            'success': False,
            'message': 'Неверный логин или пароль'
        }), 401
    
    # Защита от фиксации сессии
    session.clear()
    session['user_id'] = user['id']
    session['role'] = user['role']
    session['login'] = user['login']
    
    log_action('login_success', {'user_id': user['id']})
    
    return jsonify({
        'success': True,
        'role': user['role'],
        'redirect': '/admin' if user['role'] == 'admin' else '/dashboard'
    }), 200


@auth_bp.route('/logout', methods=['POST'])
def logout():
    log_action('logout', {'user_id': session.get('user_id')})
    session.clear()
    return jsonify({'success': True}), 200