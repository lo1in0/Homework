def levenstein(str_1, str_2):
    #Вычисляет расстояние Левенштейна между двумя строками
    n, m = len(str_1), len(str_2)
    if n > m:
        str_1, str_2 = str_2, str_1
        n, m = m, n
    current_row = range(n + 1)
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if str_1[j - 1] != str_2[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)
    return current_row[n]

def min_distance_substring(query, text):
    #Вычисляет минимальное расстояние Левенштейна между запросом и любым подстрокой текста
    query_len = len(query)
    text_len = len(text)
    
    #Если текст короче запроса, то сравниваем целиком
    if text_len < query_len:
        return levenstein(query, text)
    
    min_dist = float('inf')
    
    #Проверяем все подстроки длиной query_len
    for i in range(text_len - query_len + 1):
        substring = text[i:i + query_len]
        dist = levenstein(query, substring)
        if dist < min_dist:
            min_dist = dist
        #Если нашли точное совпадение, можно остановиться
        if min_dist == 0:
            break
    
    return min_dist

def fuzzy_search(user_query, products):
    best_matches = {}
    
    #Главный цикл сравнения
    for query in user_query:
        for item in products:
            #Приведение к нижнему регистру
            query_low = query.lower()
            item_low = item.lower()
            
            #Вычисление минимального расстояния среди всех подстрок
            dist = min_distance_substring(query_low, item_low)
            
            #Занесение в словарь с проверкой на минимальность
            #Если товара ещё нет или найдено расстояние меньше старого, то обновляем
            if item not in best_matches or dist < best_matches[item]:
                best_matches[item] = dist

    #Превращаем словарь в список кортежей и сортируем
    candidates = list(best_matches.items())
    candidates.sort(key=lambda x: x[1])
    
    #Возвращаем лучшего и три после
    return candidates[:4]

if __name__ == "__main__":
    #Тестовые данные
    user_query = ["ноут"]
    products = [
        "Ноутбук ASUS", "Смартфон Samsung", "Телефон iPhone",
        "Ноутбук HP", "Планшет iPad", "Чехол", "Умные часы"
    ]
    
    print(f"Запрос: {user_query}\n")
    
    results = fuzzy_search(user_query, products)
    
    print("Топ-4 найденных совпадений:")
    for i, (item, dist) in enumerate(results, 1):
        print(f"{i}. {item:25} | Расстояние: {dist}")