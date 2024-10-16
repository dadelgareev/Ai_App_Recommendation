import requests
from bs4 import BeautifulSoup

def fetch_product_data(main_url, preload_url):
    # Заголовки
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
    }

    # Создаем сессию
    session = requests.Session()

    # 1. Выполняем первый запрос к основной странице (инициализируем сессию)
    main_response = session.get(main_url, headers=headers)
    if main_response.status_code == 200:
        print("Первый запрос к основной странице выполнен успешно.")
    else:
        print(f"Ошибка при выполнении первого запроса: {main_response.status_code}")
        return

    # 2. Выполняем запрос к preload URL
    preload_response = session.get(preload_url, headers=headers)
    if preload_response.status_code == 200:
        print("Запрос к preload_url выполнен успешно.")
    else:
        print(f"Ошибка при выполнении запроса preload_url: {preload_response.status_code}")
        return

    # 3. Выполняем повторный запрос к основной странице для получения обновлённого результата
    final_response = session.get(main_url, headers=headers)
    if final_response.status_code == 200:
        # Разбираем HTML-код страницы с помощью BeautifulSoup
        soup = BeautifulSoup(final_response.text, 'html.parser')

        # Находим контейнер с товарами
        grid_catalog = soup.find('div', class_='grid__catalog')

        # Проверяем, что контейнер найден
        if grid_catalog:
            # Находим все карточки товаров
            product_cards = grid_catalog.find_all('div', class_='x-product-card__card')

            for product_card in product_cards:
                # Найти изображение (учитываем lazy loading, поэтому ищем не только src, но и data-src)
                product_image = product_card.find('img', class_='x-product-card__pic-img')
                if product_image:
                    # Проверяем атрибуты изображения
                    image_src = product_image.get('data-src', product_image.get('src', 'Изображение не найден'))
                else:
                    image_src = 'Изображение не найден'

                # Найти ссылку на продукт
                product_link = product_card.find('a', class_='x-product-card__link')
                product_id = product_link.get('href', 'ID не найден').split('/')[-2] if product_link else 'ID не найден'

                # Найти цену
                price_new = product_card.find('span', class_='x-product-card-description__price-new')
                if price_new:
                    price_new = price_new.text.strip()
                else:
                    price_new = 'Цена не найдена'

                # Найти старую цену (если есть)
                price_old = product_card.find('span', class_='x-product-card-description__price-old')
                if price_old:
                    price_old = price_old.text.strip()
                else:
                    price_old = 'Старая цена не найдена'

                # Найти имя продукта
                product_name = product_card.find('div', class_='x-product-card-description__product-name')
                if product_name:
                    product_name = product_name.text.strip()
                else:
                    product_name = 'Имя не найдено'

                # Вывести результаты
                print(f'ID продукта: {product_id}')
                print(f'Изображение: {image_src}')
                print(f'Имя продукта: {product_name}')
                print(f'Новая цена: {price_new}')
                print(f'Старая цена: {price_old}')
                print('-' * 40)
        else:
            print("Не удалось найти контейнер с товарами.")

    else:
        print(f"Ошибка при выполнении запроса к основной странице: {final_response.status_code}")

# Пример использования
main_url = 'https://www.lamoda.ru/c/17/shoes-men/?sitelink=topmenuM&l=4&page=1'
preload_url = 'https://z.lmcdn.ru/ru/desktop?lid=9F024064D1AF0B67975065C0021FAA17&ab=4572%2C4595%2C4624%2C4473%2C4439%2C4498%2C4561&ab_experiments=4572%2C4595%2C4624%2C4473%2C4439%2C4498%2C4561&ab_error=0&user_gender=w&customer_id=0&auth_customer_id=0&split_buckets=v3-118-02-00-061775-061931-072168-112188-052199-082227-052232-042233-092237-012238-082244-112249-122252-072253-122254-082255-052256-052258&referrer=https%3A%2F%2Fwww.google.com%2F&referrer_name=google_page&source=google&url=%2Fc%2F15%2Fshoes-women%2F%3Fsitelink%3DtopmenuW%26l%3D4&previous_url=%2F&rnd=3156&version=1.0.0&is_webview=0&isPWA=0&is_mobile=0&release=24.10.10&es6=1&platform=desktop&action=pageview&country=ru&gender=women&cartQuantity=0&cartTotal=0&n_orders=0&chapter=catalog&type=catalog_page&page_type=catalog_page&ad_skus=1%3A972c4063-1445-433c-a6ab-dd750b75208c%3AMP002XW01DEO%3Acitrus%3B2%3A123f607d-7d3e-4187-a5ff-bb383237c958%3AMP002XM0BTRW%3Acitrus&sf=2222120&results=88420&xlog_event_id=fe8a5a91-97d8-406d-8ec7-c74f98e7cf83'

fetch_product_data(main_url, preload_url)
