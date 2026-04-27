from Class import Database
from config import db_config

#Инициализация подключения к MySQL
db = Database(db_config)

try:
    print("-" * 50)
    print("ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ КЛАССА DATABASE")
    print("-" * 50)
    
    #ФИЛЬТРАЦИЯ
    print("\n1. ФИЛЬТРАЦИЯ ДАННЫХ")
    
    #Простая фильтрация
    young_students = db.read('students', 
                            where = 'age < %s', 
                            params = (25,))
    print("Студенты моложе 25 лет:", young_students)
    
    #Фильтрация с сортировкой и лимитом
    top_students = db.read('students',
                          columns = 'name, age',
                          where = 'age >= %s',
                          params = (18,),
                          order_by = 'age DESC',
                          limit = 5)
    print("Топ 5 старших студентов:", top_students)
    
    #Множественная фильтрация
    filtered = db.read('students',
                      where = 'age > %s AND name LIKE %s',
                      params = (20, '%Иван%'))
    print("Студенты старше 20 с именем Иван:", filtered)
    
    #JOIN ЗАПРОСЫ
    print("\n2. JOIN ЗАПРОСЫ")
    
    # INNER JOIN
    inner_result = db.join_query(
        main_table = 'students',
        join_table = 'groups',
        on_condition = 'students.group_id = groups.id',
        columns = 'students.name, groups.group_name, groups.faculty',
        join_type = 'INNER'
    )
    print("INNER JOIN (студенты с группами):", inner_result)
    
    #LEFT JOIN
    left_result = db.join_query(
        main_table = 'students',
        join_table = 'groups',
        on_condition = 'students.group_id = groups.id',
        columns = 'students.name, groups.group_name',
        join_type = 'LEFT'
    )
    print("LEFT JOIN (все студенты):", left_result)
    
    #LEFT JOIN с фильтрацией
    filtered_join = db.join_query(
        main_table = 'students',
        join_table = 'groups',
        on_condition = 'students.group_id = groups.id',
        columns = 'students.name, students.age, groups.group_name',
        join_type = 'LEFT',
        where = 'students.age > %s',
        params = (20,)
    )
    print("LEFT JOIN с фильтрацией (возраст > 20):", filtered_join)
    
    #UNION ЗАПРОСЫ
    print("\n3. UNION ЗАПРОСЫ")
    
    #Объединение студентов и преподавателей
    queries = [
        "SELECT name, age, 'student' as role FROM students WHERE age > 18",
        "SELECT name, age, 'teacher' as role FROM teachers WHERE age > 25"
    ]
    
    union_result = db.union_query(queries, all=False)
    print("UNION (без дубликатов):", union_result)
    
    union_all_result = db.union_query(queries, all=True)
    print("UNION ALL (с дубликатами):", union_all_result)
    
    print("\n" + "-" * 50)
    print("Все операции выполнены успешно!")
    print("-" * 50)
    
except Exception as e:
    print(f"Ошибка: {e}")

finally:
    db.close()
    print("\nСоединение закрыто")