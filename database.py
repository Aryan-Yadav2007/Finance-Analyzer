import sqlite3

conn = sqlite3.connect("finance.db")

cursor = conn.cursor()

cursor.execute(""" 
CREATE TABLE IF NOT EXISTS transactions(
id INTEGER PRIMARY KEY AUTOINCREMENT,
amount INTEGER,
type TEXT NOT NULL,
description TEXT NOT NULL,
date TEXT
)
 """)

conn.commit()

conn.close()
