import sqlite3
conn = sqlite3.connect("ContactBDD.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
     id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
     nom TEXT,
     prenom TEXT,
     catégorie TEXT,
     teléphone TEXT,
     mail TEXT,
     adresse TEXT
)
""")
conn.commit()
conn.close()
