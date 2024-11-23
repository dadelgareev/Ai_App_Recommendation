import requests
import json
import os
import requests
from PIL import Image
from io import BytesIO

# URL для запроса
url = "https://catalog.wb.ru/catalog/men_shoes/v2/catalog?ab_testing=false&appType=1&cat=8194&curr=rub&dest=123585969&sort=popular&spp=30"


# Заголовки для запроса
headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "Origin": "https://www.wildberries.ru",
    "Priority": "u=1, i",
    "Referer": "https://www.wildberries.ru/catalog/obuv/muzhskaya/kedy-i-krossovki",
    "Sec-CH-UA": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    "Sec-CH-UA-Mobile": "?0",
    "Sec-CH-UA-Platform": '"Windows"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
}

# Отправляем GET-запрос
response = requests.get(url, headers=headers)

# Проверка успешности запроса
if response.status_code == 200:
    # Получение JSON-данных
    data = response.json()

    # Извлечение продуктов (атрибут product)
    products = data.get('data', {}).get('products', [])

    # Перебор продуктов и вывод данных
    for product in products:
        product_id = product.get('id', 'Нет ID')
        product_name = product.get('name', 'Нет имени')
        product_brand = product.get('brand', 'Нет бренда')
        product_price = product.get('priceU', 'Нет цены')  # Цена в копейках, делим на 100
        product_entity = product.get('entity', 'Нет сущности')
        rating = product.get('rating', 'Нет рейтинга')

        print(f'ID: {product_id}')
        print(f'Название: {product_name}')
        print(f'Бренд: {product_brand}')
        print(f'Цена: {product_price} руб.')
        print(f'Рейтинг: {rating}')
        print(f'Сущность: {product_entity}')
        print('-' * 40)

else:
    print(f'Не удалось получить данные. Код ответа: {response.status_code}')


def find_basket_index(vol):
    if vol <= 143:
        return "01"
    elif vol <= 287:
        return "02"
    elif vol <= 431:
        return "03"
    elif vol <= 719:
        return "04"
    elif vol <= 1007:
        return "05"
    elif vol <= 1061:
        return "06"
    elif vol <= 1115:
        return "07"
    elif vol <= 1169:
        return "08"
    elif vol <= 1313:
        return "09"
    elif vol <= 1601:
        return "10"
    elif vol <= 1655:
        return "11"
    elif vol <= 1919:
        return "12"
    elif vol <= 2045:
        return "13"
    elif vol <= 2189:
        return "14"
    elif vol <= 2405:
        return "15"
    elif vol <= 2621:
        return "16"
    elif vol <= 2837:
        return "17"
    elif vol <= 3053:
        return "18"
    else:
        return "19"

def generate_links_to_download_webp():
    data = response.json()

    products = data.get('data', {}).get('products', [])

    for product in products:
        product_id = product.get('id', 'Нет ID')
        vol = product_id // 100000
        part = product_id // 1000
        src = "https://basket-"+find_basket_index(vol) +".wbbasket.ru/vol"+str(vol)+"/part"+str(part)+"/"+str(product_id)+"/images/c516x688/1.webp"
        print(src)
        print('-' * 40)

        download_and_save_image(src, product_id)


def download_and_save_image(src, product_id):
    try:
        response = requests.get(src)
        response.raise_for_status()  # Проверяем успешность запроса
        img = Image.open(BytesIO(response.content))  # Открываем изображение из потока байтов

        # Создаем директорию для сохранения изображений, если она не существует
        save_directory = "downloaded_images"
        os.makedirs(save_directory, exist_ok=True)

        # Путь для сохранения изображения в формате PNG
        img_save_path = os.path.join(save_directory, f"{product_id}.png")

        # Конвертируем и сохраняем изображение в формате PNG
        img.convert("RGBA").save(img_save_path, "PNG")
        print(f"Image saved as: {img_save_path}")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading image: {e}")
    except Exception as e:
        print(f"Error processing image: {e}")
    finally:
        print('-' * 40)

generate_links_to_download_webp()

##https://basket-01.wbbasket.ru/vol82/part8264/8264962/images/c516x688/1.webp
##src="https://basket-16.wbbasket.ru/vol2602/part260250/260250395/images/c516x688/1.webp"