import sqlite3
import pandas as pd

#Полный путь к файлу датасета
csv_path = r'C:\Users\lopat\Desktop\1-ый курс 2-ой сем\СПОиБ\ПЗ-11\100000 Sales Records.csv'

#Чтение файла датасета
DataFrame = pd.read_csv(csv_path) #Чтение файла и превращение в таблицу
print('-'*20)
print('Прочитано')
print('-'*20)
#Создание базы данных
Connection = sqlite3.connect('Sales.db')#Создание базы данных 

DataFrame.to_sql('Sales', Connection, if_exists='replace', index=False) #Заполнение базы данных данными из таблицы
print('Загружено')
print('-'*20)
#Проверка количества загруженных записей
Cursor = Connection.cursor()
Cursor.execute('SELECT COUNT(*) FROM Sales') #Подсчет количества записей в таблице
print(f'Количество записей: {Cursor.fetchone()[0]}')
print('-'*20)

#Закрытие соединения с базой данных
Connection.close()
print('Соединение закрыто')
print('-'*20)