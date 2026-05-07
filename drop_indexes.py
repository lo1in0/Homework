import sqlite3

Connection = sqlite3.connect('Sales.db')
Cursor = Connection.cursor()

#Список имён индексов
indexes = ['idx_Region', 'idx_Country', 'idx_Item_Type', 'idx_Sales_Channel', 'idx_Order_Priority']

for index_name in indexes:
    Cursor.execute(f'DROP INDEX IF EXISTS {index_name}')
    print(f'Удалён индекс: {index_name}')

Connection.commit()
print('Сохранено')

Connection.close()
print('Соединение закрыто')