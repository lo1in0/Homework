from pathlib import Path
import os

#Автоматический поиск пути к файлу с кодом
script_dir = Path(__file__).parent

file1_path = script_dir / "file1.txt" #Построение пути файла "file1.txt"
file2_path = script_dir / "file2.txt" #Построение пути файла "file2.txt"

def calculate():

    while True:
#Чтение файлов
        try:
            with open(file1_path, 'r') as f1:
                set1 = set(f1.read().strip().split(","))

            with open(file2_path, 'r') as f2:
                set2 = set(f2.read().strip().split(","))

        except FileNotFoundError:
            print("Ошибка: Файлы file1.txt или file2.txt не найдены в папке со скриптом!")
            exit()

        #Список допустимых действий
        ops = ['Пересечение', 'Объединение', 'Разность', 'Симметрическая разность', "Закрыть кальклятор"]
        print('='*50)
        print('Доступные операции:')
        print('-'*26)
        for n, i in enumerate(ops, 1):
            print(f"{n}. {i}")
        print('='*50)

        #Цикл проверки ввода запроса от пользователя
        while True:
            try:
                ch = int(input('Выберите операцию над множеством (1-5): '))
                if 1 <= ch <= 5:
                    break #Запрос удовлитворяет условия
                else:
                    print('='*50)
                    print("❌ Введите допустимый вариант ❌")
                    print('='*50)
            except ValueError:
                print('='*50)
                print("❌ Введите корректный запрос ❌")
                print('='*50)

        #Выполнения операции в зависимости от выбора пользователя
        if ch == 1:
            print('='*50)
            print("✅ Ваш запрос принят!")
            res = set1 & set2
        elif ch == 2:
            print('='*50)
            print("✅ Ваш запрос принят!")
            res = set1 | set2
        elif ch == 3:
            print('='*50)
            print("✅ Ваш запрос принят!")
            res = set1 - set2
        elif ch == 4:
            print('='*50)
            print("✅ Ваш запрос принят!")
            res = set1 ^ set2
        elif ch == 5:
            print("✅ Ваш запрос принят!")
            print('='*50)
            print("🔚 До вчтречи!")
            print('='*50)
            res = None
            break
        else:
            res = None
            print('='*50)
            print("❌ Введите допутсимый вариант действия ❌")
        
        #Вывод результата при корректном запросе пользователя
        if res is not None:
            print('-'*50)
            print("🔽 Результат вашего запроса 🔽")
            print('-'*50)
            print(sorted(list(res)))
            print('='*50)

calculate()