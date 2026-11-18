"""Тесты маршрутов регистрации и авторизации."""
import pytest


class TestRegister:
    """Тесты регистрации."""
    
    def test_register_success(self, client):
        """Успешная регистрация."""
        response = client.post('/api/auth/register', json={
            'login': 'newuser',
            'password': 'password123',
            'email': 'new@example.ru',
            'phone': '8(999)111-22-33'
        })
        assert response.status_code == 201
        data = response.get_json()
        assert data['success'] is True
    
    def test_register_short_login(self, client):
        """Регистрация с коротким логином."""
        response = client.post('/api/auth/register', json={
            'login': 'ab',
            'password': 'password123',
            'email': 'x@y.ru',
            'phone': '8(999)111-22-33'
        })
        assert response.status_code == 400
        assert '6 символов' in response.get_json()['message']
    
    def test_register_weak_password(self, client):
        """Регистрация со слабым паролем."""
        response = client.post('/api/auth/register', json={
            'login': 'validuser',
            'password': '123',
            'email': 'x@y.ru',
            'phone': '8(999)111-22-33'
        })
        assert response.status_code == 400
    
    def test_register_invalid_email(self, client):
        """Регистрация с невалидным email."""
        response = client.post('/api/auth/register', json={
            'login': 'validuser',
            'password': 'password123',
            'email': 'not-an-email',
            'phone': '8(999)111-22-33'
        })
        assert response.status_code == 400
    
    def test_register_invalid_phone(self, client):
        """Регистрация с невалидным телефоном."""
        response = client.post('/api/auth/register', json={
            'login': 'validuser',
            'password': 'password123',
            'email': 'x@y.ru',
            'phone': '+79991112233'
        })
        assert response.status_code == 400


class TestLogin:
    """Тесты авторизации."""
    
    def test_login_success(self, client):
        """Успешный вход."""
        # Сначала регистрируемся
        client.post('/api/auth/register', json={
            'login': 'loguser',
            'password': 'password123',
            'email': 'log@example.ru',
            'phone': '8(999)111-22-33'
        })
        
        # Входим
        response = client.post('/api/auth/login', json={
            'login': 'loguser',
            'password': 'password123'
        })
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'redirect' in data
    
    def test_login_wrong_password(self, client):
        """Вход с неверным паролем."""
        client.post('/api/auth/register', json={
            'login': 'loguser2',
            'password': 'password123',
            'email': 'log2@example.ru',
            'phone': '8(999)111-22-33'
        })
        
        response = client.post('/api/auth/login', json={
            'login': 'loguser2',
            'password': 'wrong'
        })
        assert response.status_code == 401
    
    def test_login_nonexistent_user(self, client):
        """Вход несуществующего пользователя."""
        response = client.post('/api/auth/login', json={
            'login': 'nobody',
            'password': 'password123'
        })
        assert response.status_code == 401
    
    def test_admin_login(self, client):
        """Вход администратора."""
        response = client.post('/api/auth/login', json={
            'login': 'Conf2027',
            'password': 'Demo7777'  # <-- ИСПРАВИТЬ ЗДЕСЬ
        })
        assert response.status_code == 200
        data = response.get_json()
        assert data['role'] == 'admin'