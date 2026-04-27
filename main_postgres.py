from ClassPostgreSQL import DatabasePostgreSQL
from config_postgres import db_config_postgres

print("="*50)
print("ТЕСТ PostgreSQL (Windows + Docker)")
print("="*50)

db = DatabasePostgreSQL(db_config_postgres)

try:
    print("\n📖 Чтение всех студентов:")
    students = db.read('students')
    for s in students:
        print(f"  {s['id']}: {s['name']} | {s['age']} лет | {s['group_name']}")

    print("\n🔍 Фильтрация (возраст > 20):")
    filtered = db.read('students', where='age > %s', params=(20,))
    for s in filtered:
        print(f"  {s['name']} ({s['age']} лет)")

    print("\n➕ Добавление записи:")
    new_id = db.create('students', {'name': 'Козлов Дмитрий', 'age': 22, 'group_name': 'ИС-103'})

    print("\n✏️ Обновление:")
    db.update_by_id('students', new_id, {'age': 23})

    print("\n🗑️ Удаление:")
    db.delete_by_id('students', new_id)

    print("\n✅ Готово! Данные обработаны.")

except Exception as e:
    print(f"\n❌ Ошибка: {e}")

finally:
    db.close()