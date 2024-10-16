import re
import requests
from bs4 import BeautifulSoup

def fetch_product_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
    }

    # Выполняем запрос к странице
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Разбираем HTML-код страницы с помощью BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Ищем скрипт, содержащий переменную __NUXT__
        script_tag = soup.find('script', string=re.compile(r'var __NUXT__'))
        extracted_text = ""

        if script_tag:
            # Извлекаем полный текст скрипта
            script_content = script_tag.string

            # Поиск блоков для выделения текстовых данных
            matches_start = script_content.find('"products"')
            matched_end = script_content.find('settings')

            if matches_start != -1 and matched_end != -1:
                extracted_text = script_content[matches_start:matched_end]

        # Находим значение "pages" и извлекаем его
        start_index = extracted_text.find('"pages":')
        if start_index != -1:
            text_after_pages = extracted_text[start_index + len('"pages":'):]
            pages_id = text_after_pages.split(',')[0].strip()
            print(f"Количество страниц: {pages_id}")

        # Разбиваем строку для поиска картинок
        extracted_text = extracted_text.split('"')

        # Находим контейнер с товарами
        grid_catalog = soup.find('div', class_='grid__catalog')

        if grid_catalog:
            # Находим все карточки товаров
            product_cards = grid_catalog.find_all('div', class_='x-product-card__card')

            for number, product_card in enumerate(product_cards, 1):

                # Ищем ссылку на продукт внутри карточки
                product_link = product_card.find('a', class_='x-product-card__link')
                product_url = product_link.get('href', 'URL не найден') if product_link else 'URL не найден'

                # Извлечение идентификатора продукта
                product_id = product_url.split('/')[2]
                product_id_upper = product_id.upper() + "_"

                # Поиск изображений, связанных с продуктом
                matching_pics = [pic for pic in extracted_text if product_id_upper in pic and (pic.endswith('.jpg') or pic.endswith('.jpeg'))]

                for i in range(len(matching_pics)):
                    matching_pics[i] = "https://a.lmcdn.ru/img236x341" + matching_pics[i]

                # Извлечение данных продукта
                product_image = product_card.find('img', class_='x-product-card__pic-img')
                image_src = product_image.get('data-src', product_image.get('src', 'Изображение не найден')) if product_image else 'Изображение не найден'

                price_new = product_card.find('span', class_='x-product-card-description__price-new')
                price_new = price_new.text.strip() if price_new else 'Цена не найдена'

                price_old = product_card.find('span', class_='x-product-card-description__price-old')
                price_old = price_old.text.strip() if price_old else 'Старая цена не найдена'

                product_name = product_card.find('div', class_='x-product-card-description__product-name')
                product_name = product_name.text.strip() if product_name else 'Имя не найдено'

                # Вывод результатов
                print(f'Номер: {number}')
                print(f'Ссылка на товар: {product_url}')
                print(f'ID продукта: {product_id}')
                print(f'Изображение: {image_src}')
                print(f'Имя продукта: {product_name}')
                print(f'Новая цена: {price_new}')
                print(f'Старая цена: {price_old}')
                print(matching_pics)
                print('-' * 40)

        else:
            print("Не удалось найти контейнер с товарами.")
    else:
        print(f"Ошибка при выполнении запроса: {response.status_code}")

# Пример использования
url = 'https://www.lamoda.ru/c/17/shoes-men/?sitelink=topmenuM&l=4&page=1'
fetch_product_data(url)
