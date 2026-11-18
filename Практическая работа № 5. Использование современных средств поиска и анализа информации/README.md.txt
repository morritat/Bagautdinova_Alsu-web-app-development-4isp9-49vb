# 1. Обновить pip
python -m pip install --upgrade pip

# 2. Установить pytest
pip install pytest pytest-cov

# 3. Проверить установку
pytest --version

# 4. Запустить все тесты
python -m pytest -v

# 5. Запустить с покрытием
python -m pytest --cov=backend --cov-report=term-missing



# 🚀 Инструкция по настройке и запуску проекта «Конференции.РФ»

Этот файл содержит пошаговое руководство по созданию необходимых конфигураций и запуску веб-приложения на Windows.

---

## 📁 ШАГ 1: Создание файла `.gitignore`

Этот файл запрещает Git загружать в репозиторий лишние и секретные файлы (виртуальное окружение, кэш, базу данных).

**Где создать:** В папке `conference_portal` (там же, где лежат папки `backend/`, `frontend/` и файл `schema.sql`).


**Содержимое файла `.gitignore.py`:**
```text
venv/
__pycache__/
*.pyc
database/conference.db
.env
*.log
.vscode/
.idea/
Thumbs.db
desktop.ini



# 5. Создать и инициализировать базу данных
python init_db.py

# 6. Запустить веб-приложение
python -m backend.app
