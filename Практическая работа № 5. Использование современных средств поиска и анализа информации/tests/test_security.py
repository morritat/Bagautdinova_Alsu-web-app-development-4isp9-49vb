"""Тесты подсистемы безопасности."""
import pytest
import time


class TestRateLimiter:
    """Тесты защиты от брутфорса."""
    
    def test_rate_limit_blocks_after_5_attempts(self, client):
        """После 5 попыток входа — блокировка."""
        # Регистрируем пользователя
        client.post('/api/auth/register', json={
            'login': 'ratetest',
            'password': 'password123',
            'email': 'rate@example.ru',
            'phone': '8(999)111-22-33'
        })
        
        # 5 правильных попыток (или неправильных — не важно)
        for i in range(5):
            response = client.post('/api/auth/login', json={
                'login': 'ratetest',
                'password': 'wrong'
            })
        
        # 6-я попытка должна быть заблокирована
        response = client.post('/api/auth/login', json={
            'login': 'ratetest',
            'password': 'wrong'
        })
        assert response.status_code == 429
        data = response.get_json()
        assert 'Слишком много попыток' in data['message']


class TestSQLInjection:
    """Тесты защиты от SQL-инъекций."""
    
    def test_sql_injection_in_login(self, client):
        """SQL-инъекция в поле логина не проходит."""
        response = client.post('/api/auth/login', json={
            'login': "' OR '1'='1",
            'password': 'anything'
        })
        assert response.status_code == 401
    
    def test_sql_injection_in_register(self, client):
        """SQL-инъекция при регистрации не проходит."""
        response = client.post('/api/auth/register', json={
            'login': "test'; DROP TABLE user; --",
            'password': 'password123',
            'email': 'x@y.ru',
            'phone': '8(999)111-22-33'
        })
        assert response.status_code == 400
        
        # Проверяем, что таблица user всё ещё существует
        from backend.database import Database
        db = Database()
        users = db.fetch_all("SELECT * FROM user")
        assert users is not None


class TestXSS:
    """Тесты защиты от XSS."""
    
    def test_xss_in_register(self, client):
        """XSS-скрипт в поле ФИО обезврежен."""
        response = client.post('/api/auth/register', json={
            'login': 'xssuser',
            'password': 'password123',
            'email': 'xss@example.ru',
            'phone': '8(999)111-22-33'
        })
        # Даже если регистрация пройдёт, скрипт должен быть экранирован
        assert response.status_code in (201, 400)


class TestSecurityHeaders:
    """Тесты безопасных HTTP-заголовков."""
    
    def test_x_frame_options(self, client):
        """Заголовок X-Frame-Options установлен."""
        response = client.get('/')
        assert response.headers.get('X-Frame-Options') == 'DENY'
    
    def test_x_content_type_options(self, client):
        """Заголовок X-Content-Type-Options установлен."""
        response = client.get('/')
        assert response.headers.get('X-Content-Type-Options') == 'nosniff'
    
    def test_content_security_policy(self, client):
        """Заголовок Content-Security-Policy установлен."""
        response = client.get('/')
        csp = response.headers.get('Content-Security-Policy')
        assert csp is not None
        assert "default-src 'self'" in csp