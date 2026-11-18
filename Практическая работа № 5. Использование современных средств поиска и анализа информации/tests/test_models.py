"""Тесты моделей User, Event, Request."""
import pytest
from backend.models.user import User
from backend.models.event import Event
from backend.models.request import Request
from backend.database import Database


class TestUserModel:
    """Тесты модели User."""
    
    def test_create_user(self, test_db):
        """Создание валидного пользователя."""
        user = User(
            login='newuser',
            password='password123',
            email='new@example.ru',
            phone='8(999)222-33-44'
        )
        ok, result = user.save()
        assert ok is True
        assert isinstance(result, int)
    
    def test_duplicate_login(self, test_db):
        """Попытка создать пользователя с существующим логином."""
        User(login='dupuser', password='password123',
             email='a@b.ru', phone='8(999)111-22-33').save()
        
        user2 = User(login='dupuser', password='password123',
                     email='c@d.ru', phone='8(999)444-55-66')
        ok, msg = user2.save()
        assert ok is False
        assert 'логином' in msg
    
    def test_duplicate_email(self, test_db):
        """Попытка создать пользователя с существующим email."""
        User(login='userone', password='password123',
             email='same@example.ru', phone='8(999)111-22-33').save()
        
        user2 = User(login='usertwo', password='password123',
                     email='same@example.ru', phone='8(999)444-55-66')
        ok, msg = user2.save()
        assert ok is False
        assert 'email' in msg
    
    def test_short_login(self, test_db):
        """Логин короче 6 символов."""
        user = User(login='abc', password='password123',
                    email='x@y.ru', phone='8(999)111-22-33')
        ok, msg = user.save()
        assert ok is False
        assert '6 символов' in msg
    
    def test_invalid_phone(self, test_db):
        """Неверный формат телефона."""
        user = User(login='validuser', password='password123',
                    email='x@y.ru', phone='+79991112233')
        ok, msg = user.save()
        assert ok is False
        assert 'формат' in msg.lower() or '8(' in msg
    
    def test_authenticate_success(self, test_db):
        """Успешная авторизация."""
        User(login='authuser', password='secret123',
             email='auth@example.ru', phone='8(999)111-22-33').save()
        
        user = User.authenticate('authuser', 'secret123')
        assert user is not None
        assert user['login'] == 'authuser'
    
    def test_authenticate_wrong_password(self, test_db):
        """Неверный пароль при авторизации."""
        User(login='authusertwo', password='secret123',
             email='auth2@example.ru', phone='8(999)111-22-33').save()
        
        user = User.authenticate('authusertwo', 'wrong')
        assert user is None


class TestEventModel:
    """Тесты модели Event."""
    
    def test_create_event(self, test_db):
        """Создание мероприятия."""
        event = Event(
            name='Аудитория №101',
            date='2027-06-15',
            place='Аудитория',
            description='Большая аудитория'
        )
        event_id = event.save()
        assert isinstance(event_id, int)
    
    def test_get_all_events(self, test_db):
        """Получение списка всех мероприятий."""
        Event(name='Event 1', date='2027-01-01', place='A', description='').save()
        Event(name='Event 2', date='2027-02-01', place='B', description='').save()
        
        events = Event.get_all()
        assert len(events) >= 2


class TestRequestModel:
    """Тесты модели Request."""
    
    def test_create_request(self, test_db):
        """Создание заявки."""
        user = User(login='requser', password='password123',  # <-- убрали _
                    email='req@example.ru', phone='8(999)111-22-33')
        user.save()
        
        event = Event(name='Room', date='2027-01-01', place='A', description='')
        event.save()
        
        req = Request(user_id=user.id, event_id=event.id, status_id=1)
        req_id = req.save()
        assert isinstance(req_id, int)

    def test_get_by_user(self, test_db):
        """Получение заявок пользователя."""
        user = User(login='requsertwo', password='password123',  # <-- убрали _
                    email='req2@example.ru', phone='8(999)111-22-33')
        user.save()
        
        event = Event(name='Room2', date='2027-01-01', place='A', description='')
        event.save()
        
        Request(user_id=user.id, event_id=event.id, status_id=1).save()
        
        requests = Request.get_by_user(user.id)
        assert len(requests) >= 1