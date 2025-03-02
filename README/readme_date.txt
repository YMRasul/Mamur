1. �������� �������

import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# ������ ������� � �����
cursor.execute("""
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    event_date TEXT NOT NULL  -- ������ ���� � ������� YYYY-MM-DD
)
""")

conn.commit()
conn.close()



2. ���������� ���� � ��

from datetime import datetime

def save_event(name: str, date: str):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO events (name, event_date) VALUES (?, ?)", (name, date))
    conn.commit()
    conn.close()

# ������ ���������� �������
save_event("������� � ��������", "2025-02-28")
save_event("���� ��������", "2025-03-10")
save_event("�������������", "2025-02-25")


3. ��������� ��������������� ������

def get_sorted_events():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # �������� ������, ��������������� �� ����
    cursor.execute("SELECT name, event_date FROM events ORDER BY event_date ASC")
    events = cursor.fetchall()

    conn.close()
    return events

# ������� ��������������� �������
for event in get_sorted_events():
    print(event)


('�������������', '2025-02-25')
('������� � ��������', '2025-02-28')
('���� ��������', '2025-03-10')


4. �������������: ���������� ������� �� ����

def get_events_by_date(date: str):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM events WHERE event_date = ?", (date,))
    events = cursor.fetchall()

    conn.close()
    return events

print(get_events_by_date("2025-02-28"))



�����

���������� ������ YYYY-MM-DD (SQLite ��������� ��������� ���).
������ � TEXT, �� ����� � � DATETIME.
��������� � ������� ORDER BY event_date ASC.
