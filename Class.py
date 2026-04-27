import mysql.connector

class Database:
    
    def __init__(self, config):

        self.connection = mysql.connector.connect(**config)
        self.cursor = self.connection.cursor(dictionary=True)
        print("Подключение к MySQL установлено")
    
    def close(self):

        self.cursor.close()
        self.connection.close()
        print("Соединение закрыто")
    
    #CREATE
    def create(self, table, data):

        columns = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = f"INSERT INTO {table} ({columns}) VALUES ({values})"
        
        self.cursor.execute(sql, list(data.values()))
        self.connection.commit()
        
        print(f"Запись добавлена, ID: {self.cursor.lastrowid}")
        return self.cursor.lastrowid
    
    #READ с фильтрацией
    def read(self, table, columns='*', where=None, params=None, order_by=None, limit=None):

        sql = f"SELECT {columns} FROM {table}"
        
        query_params = []
        
        if where:
            sql += f" WHERE {where}"
            if params:
                query_params.extend(params if isinstance(params, list) else [params])
        
        if order_by:
            sql += f" ORDER BY {order_by}"
        
        if limit:
            sql += f" LIMIT %s"
            query_params.append(limit if isinstance(limit, int) else int(limit))
        
        self.cursor.execute(sql, query_params if query_params else None)
        return self.cursor.fetchall()
    
    def read_one(self, table, id, id_column='id'):
  
        sql = f"SELECT * FROM {table} WHERE {id_column} = %s"
        self.cursor.execute(sql, (id,))
        return self.cursor.fetchone()
    
    #UPDATE
    def update(self, table, data, where, where_params=None):

        set_clause = ', '.join([f"{key} = %s" for key in data.keys()])
        sql = f"UPDATE {table} SET {set_clause} WHERE {where}"
        
        values = list(data.values())
        if where_params:
            values.extend(where_params if isinstance(where_params, list) else [where_params])
        
        self.cursor.execute(sql, values)
        self.connection.commit()
        
        print(f"Обновлено записей: {self.cursor.rowcount}")
        return self.cursor.rowcount
    
    def update_by_id(self, table, id, data, id_column='id'):

        set_clause = ', '.join([f"{key} = %s" for key in data.keys()])
        sql = f"UPDATE {table} SET {set_clause} WHERE {id_column} = %s"
        
        values = list(data.values()) + [id]
        self.cursor.execute(sql, values)
        self.connection.commit()
        
        print(f"Запись с ID {id} обновлена")
        return self.cursor.rowcount
    
    #DELETE
    def delete(self, table, where, params=None):

        sql = f"DELETE FROM {table} WHERE {where}"
        self.cursor.execute(sql, params if params else None)
        self.connection.commit()
        
        print(f"Удалено записей: {self.cursor.rowcount}")
        return self.cursor.rowcount
    
    def delete_by_id(self, table, id, id_column='id'):
        
        sql = f"DELETE FROM {table} WHERE {id_column} = %s"
        self.cursor.execute(sql, (id,))
        self.connection.commit()
        
        print(f"Запись с ID {id} удалена")
        return self.cursor.rowcount
    
    #JOIN запросы
    def join_query(self, main_table, join_table, on_condition, 
                   columns='*', join_type='INNER', where=None, params=None):

        join_types = {
            'INNER': 'INNER JOIN',
            'LEFT': 'LEFT JOIN',
            'RIGHT': 'RIGHT JOIN',
            'FULL': 'FULL OUTER JOIN',
            'CROSS': 'CROSS JOIN'
        }
        
        join_clause = join_types.get(join_type.upper(), 'INNER JOIN')
        sql = f"SELECT {columns} FROM {main_table} {join_clause} {join_table} ON {on_condition}"
        
        if where:
            sql += f" WHERE {where}"
        
        self.cursor.execute(sql, params if params else None)
        return self.cursor.fetchall()
    
    #UNION запросы
    def union_query(self, queries, all=False):
        """
        queries: список SQL-запросов (строки)
        all: если True, использует UNION ALL (сохраняет дубликаты)
        """

        union_type = "UNION ALL" if all else "UNION"
        sql = f" {union_type} ".join(queries)
        
        self.cursor.execute(sql)
        return self.cursor.fetchall()


#ПРИМЕР ИСПОЛЬЗОВАНИЯ
if __name__ == "__main__":
    from config import db_config
    
    db = Database(db_config)
    
    try:
        print("\n--- ПРИМЕРЫ ФИЛЬТРАЦИИ ---")
        
        #Все студенты старше 18 лет
        students = db.read('students', 
                          where = 'age > %s', 
                          params = (18,))
        print("Студенты старше 18:", students)
        
        #Студенты с сортировкой и лимитом
        students = db.read('students',
                          columns = 'name, age',
                          order_by = 'age DESC',
                          limit = 5)
        print("Топ 5 старших студентов:", students)
        
        print("\nПРИМЕРЫ JOIN")
        
        #INNER JOIN
        result = db.join_query(
            main_table = 'students',
            join_table = 'groups',
            on_condition = 'students.group_id = groups.id',
            columns = 'students.name, groups.group_name',
            join_type = 'INNER'
        )

        print("INNER JOIN результат:", result)
        
        #LEFT JOIN с фильтрацией
        result = db.join_query(
            main_table = 'students',
            join_table = 'groups',
            on_condition = 'students.group_id = groups.id',
            columns = 'students.name, students.age, groups.group_name',
            join_type = 'LEFT',
            where = 'students.age > %s',
            params = (20,)
        )

        print("LEFT JOIN с фильтрацией:", result)
        
        print("\nПРИМЕР UNION")
        
        queries = [    
            "SELECT name, age, 'student' as type FROM students WHERE age > 18",
            "SELECT name, age, 'teacher' as type FROM teachers WHERE age > 25"
        ]

        result = db.union_query(queries, all=True)
        print("UNION ALL результат:", result)
        
    finally:
        db.close()