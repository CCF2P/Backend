import sqlite3

con = sqlite3.connect("./library.db")

cursor = con.cursor()

cursor.execute("SELECT * FROM author")
print(cursor.fetchall())

con.close()
