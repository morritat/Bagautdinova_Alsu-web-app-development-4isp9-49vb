"""Санитизация пользовательского ввода."""
import re
import html


def sanitize_input(value: str) -> str:
    """Очищает строку от опасных символов."""
    if not isinstance(value, str):
        return value
    # Экранируем HTML-символы (защита от XSS)
    value = html.escape(value.strip())
    # Удаляем управляющие символы
    value = re.sub(r'[\x00-\x1f\x7f]', '', value)
    return value


def is_safe_sql_input(value: str) -> bool:
    """Проверяет, не содержит ли ввод SQL-инъекций."""
    if not isinstance(value, str):
        return True
    dangerous_patterns = [
        r"'\s*OR\s*'",
        r"--",
        r";",
        r"UNION\s+SELECT",
        r"DROP\s+TABLE",
        r"INSERT\s+INTO",
    ]
    for pattern in dangerous_patterns:
        if re.search(pattern, value, re.IGNORECASE):
            return False
    return True


def sanitize_dict(data: dict) -> dict:
    """Санитизирует все строковые значения в словаре."""
    result = {}
    for key, value in data.items():
        if isinstance(value, str):
            result[key] = sanitize_input(value)
        else:
            result[key] = value
    return result