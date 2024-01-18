import sqlite3

connect = sqlite3.connect("./final_project.db")
cursor = connect.cursor()

cursor.execute('''
    INSERT INTO destination VALUES (1, 'Уссурийск');
    INSERt INTO destination VALUES (2, 'Иркутск');
    INSERT INTO destination VALUES (3, 'Артем');
    INSERT INTO destination VALUES (4, 'Хутор Попки');
    INSERT INTO destination VALUES (5, 'Бухалово');
    INSERT INTO destination VALUES (6, 'Пуково');
    INSERT INTO destination VALUES (7, 'Хреновое');
    INSERT INTO destination VALUES (8, 'Безбожник');
    INSERT INTO destination VALUES (9, 'Елбань');
    INSERT INTO destination VALUES (10, 'Зюзя');
    INSERT INTO destination VALUES (11, 'Морозилка');
    INSERT INTO destination VALUES (12, 'Гавнозера');
    INSERT INTO destination VALUES (13, 'Сучкино');
    INSERT INTO destination VALUES (14, 'Тупица');
    INSERT INTO destination VALUES (15, 'Чуваки');
    INSERT INTO destination VALUES (16, 'Горшки');
    INSERT INTO destination VALUES (17, 'Рожки');
    INSERT INTO destination VALUES (18, 'Комары');
    INSERT INTO destination VALUES (19, 'Путино');
    INSERT INTO destination VALUES (20, 'Херота');
''')

cursor.execute('''
    INSERT INTO stage VALUES (1, 'Ремонт');
    INSERT INTO stage VALUES (2, 'Заправка');
    INSERT INTO stage VALUES (3, 'Предполетный осмотр');
    INSERT INTO stage VALUES (4, 'Контрольный осмотр');
    INSERT INTO stage VALUES (5, 'Готов');
''')

cursor.execute('''
    INSERT INTO airplane VALUES (1, 'Airbus', 100, 1, 1);
    INSERT INTO airplane VALUES (2,	'BOEING', 100, 2, 2);
    INSERT INTO airplane VALUES (3,	'Airbus Helicopters', 55, 3, 3);
    INSERT INTO airplane VALUES (4,	'Airbus', 98, 1, 4);
    INSERT INTO airplane VALUES (5,	'BOEING', 99, 1, 5);
''')

cursor.execute('''
    INSERT INTO flight VALUES (1, '2024-04-16 08:24:18.217098', 1, 1);
    INSERT INTO flight VALUES (2, '2024-05-16 08:24:18.217098',	19,	2);
    INSERT INTO flight VALUES (3, '2024-05-10 08:24:18.217098',	16,	3);
    INSERT INTO flight VALUES (4, '2024-05-17 08:24:18.217098',	12,	4);
    INSERT INTO flight VALUES (5, '2024-06-14 08:24:18.217098',	17,	5);
    INSERT INTO flight VALUES (6, '2024-06-14 08:24:18.217098',	13,	1);
    INSERT INTO flight VALUES (7, '2024-06-16 08:24:18.217098',	13,	2);
    INSERT INTO flight VALUES (8, '2024-07-16 08:24:18.217098',	20,	3);
    INSERT INTO flight VALUES (9, '2024-07-16 08:24:18.217098',	4,	4);
    INSERT INTO flight VALUES (10, '2024-07-16 08:24:18.217098', 2,	5);
    INSERT INTO flight VALUES (11, '2024-04-16 08:24:18.217098', 1,	1);
''')

cursor.close()
connect.commit()