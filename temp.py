import sqlite3
from datetime import datetime, timedelta

# Połącz z bazą danych SQLite
conn = sqlite3.connect('baza_danych.db')
c = conn.cursor()


current_date = datetime.today()

# Oblicz różnicę w dniach do najbliższego poniedziałku
days_until_next_monday = (1 - current_date.weekday()) % 7
days_until_next_tuesday = (1 - current_date.weekday()) % 7
days_until_next_wednesday = (2 - current_date.weekday()) % 7


# Dodaj rekordy do tabeli "terminarz"
for i in range(30):  # Wstaw 10 rekordów jako przykład
    next_date = current_date + timedelta(days=days_until_next_monday + i*7)
    formatted_date = next_date.strftime('%Y-%m-%d')

    c.execute('INSERT INTO terminarz (data, godzina) VALUES (?, ?)', (formatted_date, '14:00'))
    c.execute('INSERT INTO terminarz (data, godzina) VALUES (?, ?)', (formatted_date, '15:00'))
    c.execute('INSERT INTO terminarz (data, godzina) VALUES (?, ?)', (formatted_date, '16:00'))
    c.execute('INSERT INTO terminarz (data, godzina) VALUES (?, ?)', (formatted_date, '17:00'))
    c.execute('INSERT INTO terminarz (data, godzina) VALUES (?, ?)', (formatted_date, '18:00'))
    c.execute('INSERT INTO terminarz (data, godzina) VALUES (?, ?)', (formatted_date, '19:00'))


# Zatwierdź zmiany i zamknij połączenie z bazą danych
conn.commit()
conn.close()