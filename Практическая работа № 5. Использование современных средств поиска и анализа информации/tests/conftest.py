"""Фикстуры pytest для тестов ИС «Конференции.РФ»."""
import os
import sys
import pytest
import tempfile
import gc

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import app
import backend.database as db_module
from backend.security.rate_limiter import login_limiter

@pytest.fixture(autouse=True)
def reset_rate_limiter():
    """Сбрасывает rate limiter перед каждым тестом."""
    login_limiter.requests.clear()
    yield

@pytest.fixture(scope='function')
def test_db():
    """Создаёт временную тестовую базу данных."""
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    
    # Гарантированно сбрасываем синглтон перед созданием нового
    db_module.Database._instance = None
    db = db_module.Database(db_path)
    
    with open('schema.sql', 'r', encoding='utf-8') as f:
        db.get_connection().executescript(f.read())
    
    # Создаем админа для тестов (пароль 8 символов для прохождения валидации)
    from backend.models.user import User
    admin = User(
        login='Conf2027', 
        password='Demo7777',  
        email='admin@conf2027.ru', 
        phone='8(999)000-00-00', 
        role='admin'
    )
    admin.save()
    
    yield db
    
    # === БЕЗОПАСНАЯ ОЧИСТКА ===
    db.close()               # 1. Закрываем подключение и сбрасываем синглтон внутри класса
    gc.collect()             # 2. Принудительно освобождаем ресурсы
    
    os.close(db_fd)
    try:
        os.unlink(db_path)   # 3. Удаляем файл (теперь Windows точно это позволит)
    except PermissionError:
        pass  # Игнорируем, если ОС всё ещё держит файл долю секунды


@pytest.fixture
def client(test_db):
    """Тестовый клиент Flask."""
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test_secret_key_for_pytest'
    with app.test_client() as test_client:
        with app.app_context():
            yield test_client


@pytest.fixture
def auth_client(client):
    """Авторизованный клиент (обычный пользователь)."""
    client.post('/api/auth/register', json={
        'login': 'testuser',
        'password': 'password123',
        'email': 'test@example.ru',
        'phone': '8(999)111-22-33'
    })
    client.post('/api/auth/login', json={
        'login': 'testuser',
        'password': 'password123'
    })
    return client


@pytest.fixture
def admin_client(client):
    """Авторизованный клиент (администратор)."""
    client.post('/api/auth/login', json={
        'login': 'Conf2027',
        'password': 'Demo7777'
    })
    return client