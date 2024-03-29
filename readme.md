# Концептуальная модель
![](/images/Диаграмма_базы_данных-Концептуальная.png)

На основе анализа предметной области "Запись на авиарейс", были выделены следующие информационные объекты, которые необходимо хранить в базе данных:
1. Обслуживающая бригада (maintenance_crew):
    - maintenance_id (integer, PK) - идентификатор обслуживащей бригады
    - name (VARCHAR(100)) - название бригады
2. Самолеты (airplane)
    - airplane_id (integer, PK) - идентификатор самолета
    - type (VARCHAR(100)) - тип самолета
    - number (integer) - номер самолета
    - maintenance_id (integer, FK) - внешний ключ, связанный с таблицей "maintenance_crew"
    - condition (integer) - состояние самолета, от 0 до 100
3. Место прибытия рейса (destination)
    - destination_id (integer, PK) - идентификатор места прибытия рейса
    - destination (VARCHAR(100)) - название места прибытия
4. Вылеты (flight)
    - flight_id (integer, PK) - идентификатор вылетов
    - departure_time (datatime) - время и дата вылета
    - destination_id (integer, FK) - внешний ключ, связанный с таблицей "destination"
    - airplane_id (integer, FK) - внешний ключ, связанный с таблицей "airplane"
5. Этап подготовки самолета (stage)
    - stage_id (integer, PK) - идентификатор этапа
    - name (VARCHAR(100)) - название этапа


# Логическая модель
На основе концептуальной модели, была построена логическая модель базы данных

![](/images/Диаграмма_базы_данных-Логическая.png)


# Пользователи

## Обслуживающая бригада

Функциональные возможности:
- Просмотреть самолеты, за которые отвечает бригада
- Починить самолет
- Сменить этап подготовки самолета

## Администратор

Функциональные возможности:
- Просмотреть самолеты, за которые отвечает бригада
- Добавить бригаду
- Удалить бригаду
- Изменить данные бригады
- Просмотреть список самолетов
- Удалить самолет
- Добавить самолет
- Изменит данные самолета
