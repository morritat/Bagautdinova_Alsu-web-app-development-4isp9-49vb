"""Тесты маршрутов заявок."""
import pytest


class TestRequests:
    """Тесты заявок."""
    
    def test_create_request(self, auth_client):
        """Создание заявки авторизованным пользователем."""
        # Сначала создаём мероприятие
        from backend.models.event import Event
        from backend.database import Database
        db = Database()
        event_id = db.execute(
            "INSERT INTO event (name, date, place, description) VALUES (?, ?, ?, ?)",
            ('Test Room', '2027-01-01', 'A', 'Test')
        )
        
        response = auth_client.post('/create_request', json={
            'event_id': event_id
        })
        assert response.status_code == 201
        data = response.get_json()
        assert data['success'] is True
    
    def test_create_request_unauthorized(self, client):
        """Создание заявки неавторизованным пользователем."""
        response = client.post('/create_request', json={
            'event_id': 1
        })
        assert response.status_code in (302, 401)
    
    def test_get_my_requests(self, auth_client):
        """Получение списка своих заявок."""
        response = auth_client.get('/api/requests')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'requests' in data
    
    def test_dashboard_requires_auth(self, client):
        """Dashboard требует авторизации."""
        response = client.get('/dashboard')
        assert response.status_code in (302, 401)