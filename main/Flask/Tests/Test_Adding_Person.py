import sqlite3
conn = sqlite3.connect("ContactBDD.db")
cursor = conn.cursor()
cursor.execute("""
    INSERT INTO users (nom, prenom, catégorie, téléphone, mail, adresse)
    VALUES (?, ?, ?, ?, ?, ?)""")
conn.commit()
conn.close()
