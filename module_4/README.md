# Проект 4. Авиарейсы без потерь

## 4. Изучаем закономерности в данных

### Задание 4.1

База данных содержит список аэропортов практически всех крупных городов России. В большинстве городов есть только один аэропорт. Исключение составляет:
```sql
SELECT city,
       count(*)
FROM dst_project.airports
GROUP BY city
HAVING count(*) > 1
```

### Задание 4.2 

**Вопрос 1.** Таблица рейсов содержит всю информацию о прошлых, текущих и запланированных рейсах. Сколько всего статусов для рейсов определено в таблице?
```sql
SELECT count(DISTINCT status)
FROM dst_project.flights
```

**Вопрос 2.** Какое количество самолетов находятся в воздухе на момент среза в базе (статус рейса «самолёт уже вылетел и находится в воздухе»). 
```sql
SELECT count(*)
FROM dst_project.flights
WHERE status = 'Departed'
```

**Вопрос 3.** Места определяют схему салона каждой модели. Сколько мест имеет самолет модели **773** (Boeing 777-300)? 
```sql
SELECT count(*)
FROM dst_project.seats
WHERE aircraft_code = '773'
```

**Вопрос 4.** Сколько состоявшихся (фактических) рейсов было совершено между 1 апреля 2017 года и 1 сентября 2017 года?
```sql
SELECT count(*)
FROM dst_project.flights
WHERE status = 'Arrived'
  AND actual_arrival BETWEEN '2017-04-01' AND '2017-09-01'
```

### Задание 4.3

**Вопрос 1.** Сколько всего рейсов было отменено по данным базы?
```sql
SELECT count(*)
FROM dst_project.flights
WHERE status = 'Cancelled'
```

**Вопрос 2.** Сколько самолетов моделей типа Boeing, Sukhoi Superjet, Airbus находится в базе авиаперевозок?
```sql
SELECT count(*)
FROM dst_project.aircrafts
WHERE model ilike '%Boeing%'
```
```sql
SELECT count(*)
FROM dst_project.aircrafts
WHERE model ilike '%Sukhoi%Superjet%'
```
```sql
SELECT count(*)
FROM dst_project.aircrafts
WHERE model ilike '%Airbus%'
```

**Вопрос 3.** В какой части (частях) света находится больше аэропортов?
```sql
WITH ac AS
  (SELECT substring(timezone
                    FROM '(.*)/') continent
   FROM dst_project.airports)
SELECT continent,
       count(*)
FROM ac
GROUP BY continent
ORDER BY count(*)
```

**Вопрос 4.** У какого рейса была самая большая задержка прибытия за все время сбора данных? Введите id рейса (flight_id).
```sql
SELECT flight_id
FROM dst_project.flights
WHERE actual_arrival IS NOT NULL
ORDER BY actual_arrival - scheduled_arrival DESC
LIMIT 1
```

### Задание 4.4

**Вопрос 1.** Когда был запланирован самый первый вылет, сохраненный в базе данных?
```sql
SELECT min(scheduled_departure)
FROM dst_project.flights
```

**Вопрос 2.** Сколько минут составляет запланированное время полета в самом длительном рейсе? 
```sql
SELECT EXTRACT(EPOCH
               FROM max(scheduled_arrival - scheduled_departure)) / 60
FROM dst_project.flights
```

**Вопрос 3.** Между какими аэропортами пролегает самый длительный по времени запланированный рейс?
```sql
SELECT departure_airport,
       arrival_airport
FROM dst_project.flights
ORDER BY scheduled_arrival - scheduled_departure DESC
LIMIT 1
```

**Вопрос 4.** Сколько составляет средняя дальность полета среди всех самолетов в минутах? Секунды округляются в меньшую сторону (отбрасываются до минут).
```sql
SELECT trunc(EXTRACT(EPOCH
                     FROM avg(actual_arrival - actual_departure)) / 60)
FROM dst_project.flights
```

### Задание 4.5

**Вопрос 1.** Мест какого класса у SU9 больше всего? 
```sql
SELECT fare_conditions,
       count(*)
FROM dst_project.seats
WHERE aircraft_code = 'SU9'
GROUP BY fare_conditions
ORDER BY count(*) DESC
```

**Вопрос 2.** Какую самую минимальную стоимость составило бронирование за всю историю?
```sql
SELECT min(total_amount)
FROM dst_project.bookings
```

**Вопрос 3.** Какой номер места был у пассажира с `id = 4313 788533`? 
```sql
SELECT b.seat_no
FROM dst_project.tickets t
JOIN dst_project.boarding_passes b ON b.ticket_no = t.ticket_no
WHERE t.passenger_id = '4313 788533'
```

## 5. Предварительный анализ

### Задание 5.1

**Вопрос 1**. Анапа — курортный город на юге России. Сколько рейсов прибыло в Анапу за 2017 год?
```sql
SELECT count(*)
FROM dst_project.flights f
JOIN dst_project.airports p ON f.arrival_airport = p.airport_code
WHERE p.city = 'Anapa'
  AND f.status = 'Arrived'
  AND extract(YEAR
              FROM f.actual_arrival) = 2017
```

**Вопрос 2.** Сколько рейсов из Анапы вылетело зимой 2017 года?
```sql
SELECT count(*)
FROM dst_project.flights f
JOIN dst_project.airports p ON p.airport_code = f.departure_airport
WHERE p.city = 'Anapa'
  AND date_trunc('month', f.actual_departure) in ('2017-1-1',
                                                  '2017-2-1',
                                                  '2017-12-1')
```

**Вопрос 3.** Посчитайте количество отмененных рейсов из Анапы за все время.
```sql
SELECT count(*)
FROM dst_project.flights f
JOIN dst_project.airports p ON p.airport_code = f.departure_airport 
WHERE p.city = 'Anapa'
  AND f.status = 'Cancelled'
```

**Вопрос 4.** Сколько рейсов из Анапы не летают в Москву?
```sql
SELECT count(*)
FROM dst_project.flights f
JOIN dst_project.airports pd ON pd.airport_code = f.departure_airport
JOIN dst_project.airports pa ON pa.airport_code = f.arrival_airport
WHERE pd.city = 'Anapa'
  AND pa.city != 'Moscow'
```

**Вопрос 5.** Какая модель самолета летящего на рейсах из Анапы имеет больше всего мест?
```sql
SELECT c.model,
       count(*)
FROM dst_project.seats s
JOIN dst_project.aircrafts c ON c.aircraft_code = s.aircraft_code
WHERE s.aircraft_code IN
    (SELECT f.aircraft_code
     FROM dst_project.flights f
     JOIN dst_project.airports pd ON pd.airport_code = f.departure_airport
     WHERE pd.city = 'Anapa')
GROUP BY c.aircraft_code
ORDER BY count(*) DESC
```

## 6. Переходим к реальной аналитике

```sql
SELECT f.flight_id flight_id,
       extract(MONTH
               FROM f.scheduled_departure) flight_month,
       dp.city departure_city,
       dp.airport_code departure_airport,
       dp.latitude departure_latitude,
       dp.longitude departure_longitude,
       ap.city arrival_city,
       ap.airport_code arrival_airport,
       ap.latitude arrival_latitude,
       ap.longitude arrival_longitude,
       EXTRACT(EPOCH
               FROM f.actual_arrival - f.actual_departure) flight_time_seconds,
       c.model aircraft_model,
       s.count aircraft_seats_count,
       coalesce(t.count, 0) tickets_count,
       coalesce(t.amount_total, 0.0) tickets_amount_total
FROM dst_project.flights f
JOIN dst_project.airports dp ON dp.airport_code = f.departure_airport
JOIN dst_project.airports ap ON ap.airport_code = f.arrival_airport
JOIN dst_project.aircrafts c ON c.aircraft_code = f.aircraft_code
JOIN
  (SELECT aircraft_code,
          count(*) COUNT
   FROM dst_project.seats
   GROUP BY aircraft_code) s ON s.aircraft_code = c.aircraft_code
LEFT JOIN
  (SELECT flight_id,
          count(*) COUNT,
                   sum(amount) amount_total
   FROM dst_project.ticket_flights
   GROUP BY flight_id) t ON t.flight_id = f.flight_id
WHERE dp.city = 'Anapa'
  AND (date_trunc('month', f.scheduled_departure) in ('2017-01-01',
                                                      '2017-02-01',
                                                      '2017-12-01'))
  AND f.status not in ('Cancelled')
  ```

Результат в flights_from_anapa_2017_winter.csv

Обработка в lossless.ipynb

Презентацию я не делал.
