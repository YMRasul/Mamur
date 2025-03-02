1. Создание таблицы

import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Создаём таблицу с датой
cursor.execute("""
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    event_date TEXT NOT NULL  -- Храним дату в формате YYYY-MM-DD
)
""")

conn.commit()
conn.close()



2. Сохранение даты в БД

from datetime import datetime

def save_event(name: str, date: str):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO events (name, event_date) VALUES (?, ?)", (name, date))
    conn.commit()
    conn.close()

# Пример сохранения события
save_event("Встреча с клиентом", "2025-02-28")
save_event("День рождения", "2025-03-10")
save_event("Собеседование", "2025-02-25")


3. Получение отсортированных данных

def get_sorted_events():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Получаем данные, отсортированные по дате
    cursor.execute("SELECT name, event_date FROM events ORDER BY event_date ASC")
    events = cursor.fetchall()

    conn.close()
    return events

# Выводим отсортированные события
for event in get_sorted_events():
    print(event)


('Собеседование', '2025-02-25')
('Встреча с клиентом', '2025-02-28')
('День рождения', '2025-03-10')


4. Дополнительно: фильтрация событий по дате

def get_events_by_date(date: str):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM events WHERE event_date = ?", (date,))
    events = cursor.fetchall()

    conn.close()
    return events

print(get_events_by_date("2025-02-28"))



Вывод

Используем формат YYYY-MM-DD (SQLite корректно сортирует его).
Храним в TEXT, но можно и в DATETIME.
Сортируем с помощью ORDER BY event_date ASC.
