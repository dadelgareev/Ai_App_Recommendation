import requests
from bs4 import BeautifulSoup
import re
import json

# URL страницы
url = 'https://www.lamoda.ru/c/17/shoes-men/?sitelink=topmenuM&l=4'

# Заголовки для имитации запроса из браузера
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
}

# Выполняем запрос к странице
response = requests.get(url, headers=headers)

# Если запрос выполнен успешно
if response.status_code == 200:
    # Разбираем HTML-код страницы с помощью BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Ищем скрипт, содержащий переменную __NUXT__
    script_tag = soup.find('script', string=re.compile(r'var __NUXT__'))

    if script_tag:
        # Извлекаем полный текст скрипта
        script_content = script_tag.string
        print(script_content)

        matches_start = [m.start() for m in re.finditer(r'payload', script_content)]
        matched_end = [m.start() for m in re.finditer(r'settings', script_content)]

        if len(matches_start) >= 2:
            # Индекс второго вхождения слова 'payload'
            second_payload_index = matches_start[1]
            end_payload_index = matched_end[0]

            # Извлекаем текст, начиная со второго вхождения 'payload'
            extracted_text = script_content[second_payload_index:end_payload_index]


            # Выводим результат
            #print(extracted_text)
        else:
            print("Не удалось найти два вхождения 'payload'.")




        # Используем регулярное выражение для поиска данных внутри __NUXT__ (учитывая вложенные фигурные скобки)
        nuxt_data_match = re.search(r'var __NUXT__ = ({.*?});\n', script_content, re.DOTALL)
        #print()
        if nuxt_data_match:
            nuxt_data_str = nuxt_data_match.group(1)

            # Исправляем строку: заменяем одинарные кавычки на двойные и корректируем другие потенциальные несоответствия
            nuxt_data_str = nuxt_data_str.replace("'", '"')

            # Попробуем найти необработанные ключи и значения (без кавычек) и добавить кавычки вокруг них
            nuxt_data_str = re.sub(r'(\w+):', r'"\1":', nuxt_data_str)

            try:
                # Преобразуем строку в JSON-объект
                nuxt_data = json.loads(nuxt_data_str)

                # Извлекаем данные из ключа payload
                payload_data = nuxt_data.get('payload', {})

                # Выводим данные в формате JSON
                print(json.dumps(payload_data, indent=4, ensure_ascii=False))

            except json.JSONDecodeError as e:
                print(f"Ошибка при парсинге JSON: {e}")
        else:
            print("Не удалось найти данные __NUXT__ в скрипте.")
    else:
        print("Не удалось найти скрипт с переменной __NUXT__.")
else:
    print(f"Ошибка при выполнении запроса: {response.status_code}")
