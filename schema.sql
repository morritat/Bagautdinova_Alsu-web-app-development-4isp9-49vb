-- =====================================================================
-- База данных портала «Конференции.РФ»
-- Практическая работа № 2
-- Студент: Багаутдинова Алсу, группа 4ИСП9-49ВБ
-- =====================================================================

-- Включаем поддержку внешних ключей (ОБЯЗАТЕЛЬНО для SQLite!)
PRAGMA foreign_keys = ON;

-- Таблица «Пользователь»
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    login VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(18) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'user'
);

-- Таблица «Мероприятие»
CREATE TABLE IF NOT EXISTS event (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(200) NOT NULL,
    date DATE NOT NULL,
    place VARCHAR(200) NOT NULL,
    description TEXT
);

-- Таблица «Статус» (справочник)
CREATE TABLE IF NOT EXISTS status (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- Наполнение справочника статусов
INSERT OR IGNORE INTO status (name) VALUES 
    ('Новая'),
    ('Мероприятие назначено'),
    ('Завершено');

-- Таблица «Заявка»
CREATE TABLE IF NOT EXISTS request (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    event_id INTEGER NOT NULL,
    status_id INTEGER NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (event_id) REFERENCES event(id),
    FOREIGN KEY (status_id) REFERENCES status(id)
);

-- Таблица «Отзыв»
CREATE TABLE IF NOT EXISTS review (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    request_id INTEGER UNIQUE NOT NULL,
    text TEXT NOT NULL,
    rating INTEGER CHECK (rating BETWEEN 1 AND 5),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (request_id) REFERENCES request(id)
);
