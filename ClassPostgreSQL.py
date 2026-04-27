import psycopg2
from psycopg2.extras import RealDictCursor

class DatabasePostgreSQL:
    def __init__(self, config):
        self.connection = psycopg2.connect(**config)
        self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)
        print("✅ Подключение к PostgreSQL установлено")

    def close(self):
        self.cursor.close()
        self.connection.close()
        print("🔌 Соединение закрыто")

    def create(self, table, data):
        columns = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = f"INSERT INTO {table} ({columns}) VALUES ({values}) RETURNING id"
        self.cursor.execute(sql, list(data.values()))
        self.connection.commit()
        result = self.cursor.fetchone()
        print(f"✅ Запись добавлена, ID: {result['id']}")
        return result['id']

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

    def update(self, table, data, where, where_params=None):
        set_clause = ', '.join([f"{key} = %s" for key in data.keys()])
        sql = f"UPDATE {table} SET {set_clause} WHERE {where}"
        values = list(data.values())
        if where_params:
            values.extend(where_params if isinstance(where_params, list) else [where_params])
        self.cursor.execute(sql, values)
        self.connection.commit()
        print(f"✅ Обновлено записей: {self.cursor.rowcount}")
        return self.cursor.rowcount

    def update_by_id(self, table, id, data, id_column='id'):
        set_clause = ', '.join([f"{key} = %s" for key in data.keys()])
        sql = f"UPDATE {table} SET {set_clause} WHERE {id_column} = %s"
        values = list(data.values()) + [id]
        self.cursor.execute(sql, values)
        self.connection.commit()
        print(f"✅ Запись с ID {id} обновлена")
        return self.cursor.rowcount

    def delete(self, table, where, params=None):
        sql = f"DELETE FROM {table} WHERE {where}"
        self.cursor.execute(sql, params if params else None)
        self.connection.commit()
        print(f"✅ Удалено записей: {self.cursor.rowcount}")
        return self.cursor.rowcount

    def delete_by_id(self, table, id, id_column='id'):
        sql = f"DELETE FROM {table} WHERE {id_column} = %s"
        self.cursor.execute(sql, (id,))
        self.connection.commit()
        print(f"✅ Запись с ID {id} удалена")
        return self.cursor.rowcount

    def join_query(self, main_table, join_table, on_condition, 
                   columns='*', join_type='INNER', where=None, params=None):
        join_types = {
            'INNER': 'INNER JOIN', 'LEFT': 'LEFT JOIN',
            'RIGHT': 'RIGHT JOIN', 'FULL': 'FULL OUTER JOIN', 'CROSS': 'CROSS JOIN'
        }
        join_clause = join_types.get(join_type.upper(), 'INNER JOIN')
        sql = f"SELECT {columns} FROM {main_table} {join_clause} {join_table} ON {on_condition}"
        if where:
            sql += f" WHERE {where}"
        self.cursor.execute(sql, params if params else None)
        return self.cursor.fetchall()

    def union_query(self, queries, all=False):
        union_type = "UNION ALL" if all else "UNION"
        sql = f" {union_type} ".join(queries)
        self.cursor.execute(sql)
        return self.cursor.fetchall()