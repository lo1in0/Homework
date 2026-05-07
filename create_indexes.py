import sqlite3

Connection = sqlite3.connect('Sales.db') #Подключение к базе данных
Cursor = Connection.cursor() #Создание курсора для выполнения SQL-запросов
print('-'*20)
print('Подключено с курсором')
print('-'*20)

#Создание индексов
indexes = ['Region', 'Country', 'Item Type', 'Sales Channel', 'Order Priority'] #Список столбцов для создания индексов
for index in indexes:
    index_name = f'idx_{index.replace(" ", "_")}' #Замена пробелов в названии столбца на подчеркивания для имени индекса
    Cursor.execute(f'CREATE INDEX IF NOT EXISTS {index_name} ON Sales ("{index}")') #Создание индекса для каждого столбца
    print(f'Индекс для {index} создан')
print('-'*20)

#Сохранение изменений в базе данных
Connection.commit()

#Закрытие соединения с базой данных
Connection.close()
print('Соединение закрыто')
print('-'*20)
