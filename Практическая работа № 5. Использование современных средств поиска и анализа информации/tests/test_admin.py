"""Тесты маршрутов администратора."""
import pytest


class TestAdmin:
    """Тесты админ-панели."""
    
    def test_admin_panel_access(self, admin_client):
        """Администратор имеет доступ к панели."""
        response = admin_client.get('/admin')
        assert response.status_code == 200
    
    def test_admin_panel_forbidden_for_user(self, auth_client):
        """Обычный пользователь не имеет доступа к админке."""
        response = auth_client.get('/admin')
        assert response.status_code in (302, 403)
    
    def test_admin_panel_unauthorized(self, client):
        """Неавторизованный пользователь не имеет доступа."""
        response = client.get('/admin')
        assert response.status_code in (302, 401)
    
    def test_get_all_requests(self, admin_client):
        """Администратор получает все заявки."""
        response = admin_client.get('/api/admin/requests')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
    
    def test_update_status(self, admin_client):
        """Администратор меняет статус заявки."""
        # Создаём тестовую заявку
        from backend.database import Database
        db = Database()
        req_id = db.execute(
            "INSERT INTO request (user_id, event_id, status_id) VALUES (?, ?, ?)",
            (1, 1, 1)
        )
        
        response = admin_client.put(
            f'/api/admin/requests/{req_id}',
            json={'status_id': 2}
        )
        assert response.status_code == 200
    
    def test_update_status(self, admin_client):
        """Администратор меняет статус заявки."""
        from backend.models.user import User
        from backend.models.event import Event
        from backend.models.request import Request
        
        # 1. Создаём реального пользователя и мероприятие
        user = User(login='testuserreq', password='password123', email='t@t.ru', phone='8(999)111-22-33')
        user.save()
        
        event = Event(name='Room', date='2027-01-01', place='A', description='')
        event.save()
        
        # 2. Создаём заявку с реальными ID
        req = Request(user_id=user.id, event_id=event.id, status_id=1)
        req.save()
        
        # 3. Меняем статус через API
        response = admin_client.put(
            f'/api/admin/requests/{req.id}',
            json={'status_id': 2}
        )
        assert response.status_code == 200