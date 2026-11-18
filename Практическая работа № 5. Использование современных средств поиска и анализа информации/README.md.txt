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