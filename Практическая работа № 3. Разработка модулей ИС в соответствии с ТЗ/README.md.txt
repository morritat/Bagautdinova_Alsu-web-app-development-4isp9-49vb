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

ШАГ 2: Запуск проекта через терминал
# 1. Разрешить запуск скриптов (если появится красная ошибка об ограничениях)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# (Если спросит подтверждение, нажми Y и Enter)

# 2. Создать виртуальное окружение (появится папка venv)
python -m venv venv

# 3. Активировать виртуальное окружение
.\venv\Scripts\activate

# 4. Установить необходимые библиотеки (Flask и Werkzeug)
pip install Flask==2.3.3 Werkzeug==2.3.7

# 5. Создать и инициализировать базу данных
python init_db.py

# 6. Запустить веб-приложение
python -m backend.app