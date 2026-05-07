import sqlite3
import time 
import json

#Пример запросов для тестирования
QUERIES = [
    "SELECT * FROM sales LIMIT 100", #Запрос 1: получить первые 100 записей
    "SELECT COUNT(*) FROM sales", #Запрос 2: посчитать общее количество записей
    "SELECT * FROM sales WHERE Region = 'Europe'", #Запрос 3: найти все продажи в Европе
    "SELECT AVG(\"Total Profit\") FROM sales", #Запрос 4: вычислить среднюю прибыль
    "SELECT * FROM sales ORDER BY \"Total Profit\" DESC LIMIT 50", #Запрос 5: топ-50 самых прибыльных продаж
    "SELECT COUNT(*) FROM sales WHERE \"Item Type\" = 'Electronics'", #Запрос 6: посчитать продажи электроники
    "SELECT * FROM sales WHERE \"Sales Channel\" = 'Online'", #Запрос 7: все онлайн-продажи
    "SELECT MAX(\"Total Profit\"), MIN(\"Total Profit\") FROM sales", #Запрос 8: найти максимальную и минимальную прибыль
    "SELECT Region, COUNT(*) FROM sales GROUP BY Region", #Запрос 9: количество продаж по каждому региону
    "SELECT * FROM sales WHERE \"Total Profit\" > 10000", #Запрос 10: все продажи с прибылью больше 10000
]

print('-'*20)
print('Тестирование запросов')
print('-'*20)

#Подключение к базе данных
Connection = sqlite3.connect('Sales.db')
Cursor = Connection.cursor()

result = []

#Выполнение каждого запроса с замером времени
for query in QUERIES:
    start_time = time.time() #Начало замера времени

    Cursor.execute(query) #Выполнение запроса
    data = Cursor.fetchall() #Получение всех результатов запроса

    end_time = time.time() #Конец замера времени
    execution_time = end_time - start_time #Вычисление времени выполнения
    
    result.append({'query': query, 'execution_time': execution_time, 'result_count': len(data)}) #Сохранение результата
    print(f'Запрос: {query}\nВремя выполнения: {execution_time:.4f} секунд')
    print('-'*20)

with open('query_results.json', 'w') as f:
    json.dump(result, f, indent=4, ensure_ascii=False) #Сохранение результатов в JSON файл
print('Результаты сохранены')    
print('-'*20)

Connection.close()
print('Соединение закрыто')
print('-'*20)