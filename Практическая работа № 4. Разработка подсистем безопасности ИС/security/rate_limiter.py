"""Защита от брутфорса: ограничение частоты запросов."""
import time
from functools import wraps
from collections import defaultdict
from flask import request, jsonify

class RateLimiter:
    """Простой in-memory rate limiter (для продакшена — Redis)."""
    
    def __init__(self, max_requests=5, window_seconds=60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)
    
    def is_allowed(self, key: str) -> bool:
        now = time.time()
        # Удаляем устаревшие записи
        self.requests[key] = [
            t for t in self.requests[key]
            if now - t < self.window_seconds
        ]
        if len(self.requests[key]) >= self.max_requests:
            return False
        self.requests[key].append(now)
        return True
    
    def get_retry_after(self, key: str) -> int:
        if not self.requests[key]:
            return 0
        oldest = min(self.requests[key])
        return max(0, int(self.window_seconds - (time.time() - oldest)))


# Глобальный лимитер для входа: 5 попыток в минуту
login_limiter = RateLimiter(max_requests=5, window_seconds=60)


def rate_limit(limiter: RateLimiter):
    """Декоратор для ограничения частоты запросов."""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            key = request.remote_addr
            if not limiter.is_allowed(key):
                retry_after = limiter.get_retry_after(key)
                return jsonify({
                    'success': False,
                    'message': 'Слишком много попыток. Повторите позже.',
                    'retry_after': retry_after
                }), 429
            return f(*args, **kwargs)
        return wrapper
    return decorator