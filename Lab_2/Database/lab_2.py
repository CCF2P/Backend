import sqlite3
import pandas as pd


con = sqlite3.connect("..\..\\final_project\\Database\\final_project.db")
cursor = con.cursor()

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
