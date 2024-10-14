import requests
from bs4 import BeautifulSoup


def fetch_product_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        grid_catalog = soup.find('div', class_='grid__catalog')

        if grid_catalog:
            product_cards = grid_catalog.find_all('div', class_='x-product-card__card')

            for product_card in product_cards:
                # Найти изображение
                product_image = product_card.find('img', class_='x-product-card__pic-img')
                if product_image:
                    image_src = product_image.get('src', 'Изображение не найден')
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
                print(f'Цена: {price_new}')
                print('-' * 40)

    print(grid_catalog)
url = 'https://www.lamoda.ru/c/17/shoes-men/?sitelink=topmenuM&l=4&page=1'
fetch_product_data(url)
