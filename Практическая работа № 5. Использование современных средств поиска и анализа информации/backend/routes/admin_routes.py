from flask import Blueprint, request, jsonify, render_template, session
from backend.models.request import Request
from backend.security.decorators import admin_required
from backend.security.sanitizer import sanitize_dict
from backend.security.audit_log import log_action

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/admin')
@admin_required  # ← ЗАЩИТА ОТ НЕСАНКЦИОНИРОВАННОГО ДОСТУПА
def admin_panel():
    return render_template('admin.html')


@admin_bp.route('/api/admin/requests', methods=['GET'])
@admin_required
def get_all_requests():
    data = Request.get_all_with_details()
    return jsonify({'success': True, 'requests': data}), 200


@admin_bp.route('/api/admin/requests/<int:request_id>', methods=['PUT'])
@admin_required
def update_request_status(request_id):
    data = sanitize_dict(request.get_json() or {})
    status_id = int(data.get('status_id', 0))
    
    if status_id not in (1, 2, 3):
        return jsonify({'success': False, 'message': 'Некорректный статус'}), 400
    
    Request.update_status(request_id, status_id)
    log_action('status_changed', {
        'request_id': request_id,
        'new_status_id': status_id,
        'admin_id': session.get('user_id')
    })
    return jsonify({'success': True}), 200