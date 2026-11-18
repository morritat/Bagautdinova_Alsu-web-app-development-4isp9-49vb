import sqlite3
import os

os.makedirs('database', exist_ok=True)

db_path = os.path.join('database', 'conference.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON")

with open('schema.sql', 'r', encoding='utf-8') as f:
    sql_script = f.read()

cursor.executescript(sql_script)
conn.commit()
conn.close()

print("✅ База данных создана: database/conference.db")