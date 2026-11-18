import sqlite3
import os

class Database:
    """Singleton-класс для работы с SQLite."""
    _instance = None

    def __new__(cls, db_path=None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, db_path=None):
        if self._initialized:
            return
        if db_path is None:
            db_path = os.path.join(
                os.path.dirname(__file__), '..', 'database', 'conference.db'
            )
        self.db_path = os.path.abspath(db_path)
        
        # Создаем и храним ОДНО подключение на весь жизненный цикл объекта
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")
        
        self._initialized = True

    def get_connection(self):
        return self.conn

    def execute(self, query, params=()):
        cursor = self.conn.execute(query, params)
        self.conn.commit()
        return cursor.lastrowid

    def fetch_one(self, query, params=()):
        cursor = self.conn.execute(query, params)
        row = cursor.fetchone()
        return dict(row) if row else None

    def fetch_all(self, query, params=()):
        cursor = self.conn.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
        
    def close(self):
        """Явно закрывает подключение и сбрасывает синглтон."""
        if hasattr(self, 'conn'):
            self.conn.close()
        self._initialized = False
        Database._instance = None