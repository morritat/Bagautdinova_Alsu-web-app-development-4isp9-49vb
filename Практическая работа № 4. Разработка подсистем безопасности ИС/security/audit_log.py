"""Журнал аудита действий пользователей."""
import os
import json
from datetime import datetime
from flask import session, request


AUDIT_LOG_FILE = os.path.join(
    os.path.dirname(__file__), '..', '..', 'database', 'audit.log'
)


def log_action(action: str, details: dict = None):
    """Записывает действие в журнал аудита."""
    os.makedirs(os.path.dirname(AUDIT_LOG_FILE), exist_ok=True)
    
    record = {
        'timestamp': datetime.utcnow().isoformat(),
        'action': action,
        'user_id': session.get('user_id'),
        'login': session.get('login'),
        'role': session.get('role'),
        'ip': request.remote_addr if request else None,
        'method': request.method if request else None,
        'path': request.path if request else None,
        'details': details or {}
    }
    
    with open(AUDIT_LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(record, ensure_ascii=False) + '\n')