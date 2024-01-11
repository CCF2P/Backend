import sqlite3
import pandas as pd

'''
con = sqlite3.connect("storeDB.db")
f_damp = open("store.db", "r", encoding="utf-8-sig")
damp = f_damp.read()
f_damp.close()
con.executescript(damp)
con.commit()
'''

con = sqlite3.connect("./storeDB.db")

cursor = con.cursor()

# Запросы к БД
print("Задание 1")
df1 = pd.read_sql('''
SELECT buy_step.buy_id, buy_step.step_id, city.name_city
FROM buy_step, city
WHERE buy_step.step_id = 3
ORDER BY name_city ASC, buy_id ASC;
''', con)
print(df1)
'''res = cursor.fetchall()
print([description[0] for description in cursor.description])
for row in res:
    print(row)'''
print()

print("Задание 2")
df1 = pd.read_sql('''
SELECT client.name_client AS "Клиент",
	   COUNT(DISTINCT buy_book.book_id) AS "Количество книг"
FROM client, buy_book, buy
WHERE buy.client_id = client.client_id
      AND buy.buy_id = buy_book.buy_id
GROUP BY client.name_client
UNION
SELECT client.name_client, "0"
FROM client
WHERE client.client_id NOT IN (SELECT buy.client_id
                               FROM buy)
ORDER BY client.name_client;
''', con)
print(df1)
print()

print("Задание 3")
df1 = pd.read_sql('''
SELECT author.name_author AS "Автор",
	   SUM(buy_book.amount) AS "Количество_проданных_книг"
FROM buy_book, author, book
WHERE buy_book.book_id = book.book_id
  AND author.author_id = book.author_id
GROUP BY author.name_author
HAVING SUM(buy_book.amount) > (SELECT SUM(buy_book.amount)
							   FROM buy_book, book
							   WHERE book.book_id = buy_book.book_id
							   GROUP BY book.author_id);
''', con)
print(df1)
print()

print("Задание 4")
cursor.execute('''
UPDATE book
SET price = price * 1.1
WHERE 2 <= (SELECT COUNT(buy_book.book_id)
				FROM buy_book
				GROUP BY buy_book.book_id
                HAVING buy_book.book_id = book.book_id);
''')
cursor.execute("SELECT * FROM book;")
res = cursor.fetchall()
print([description[0] for description in cursor.description])
for row in res:
    print(row)
print()

print("Задание 5")
cursor.execute('''
SELECT row_number() OVER win AS "№",
       "Булгаков М.А." AS "Автор",
	   book.title AS "Книга",
       book.amount AS "Кол-во",
       rank() OVER win AS "Ранг",
       cume_dist() OVER win AS "Распределение",
       percent_rank() OVER win AS "Ранг%"
FROM author, book
WHERE author.author_id = book.author_id AND author.name_author = "Булгаков М.А."
WINDOW win AS (ORDER BY book.amount);
''')
res = cursor.fetchall()
print([description[0] for description in cursor.description])
for row in res:
    print(row)
print()

con.close()
