import sqlite3
conn = sqlite3.connect("ContactBDD.db")
cursor = conn.cursor()
cur = cursor.execute("""SELECT * from users""")
print(cur.fetchall())
conn.commit()
conn.close()
