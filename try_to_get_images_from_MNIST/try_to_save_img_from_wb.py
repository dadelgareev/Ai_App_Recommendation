import requests
from PIL import Image
from io import BytesIO


def get_images(product_id, num_images=5):
    # Определяем путь на основе ID товара
    millions = product_id // 1000000
    thousands = (product_id // 1000) % 1000

    image_urls = []

    for i in range(1, num_images + 1):  # например, пробуем 5 изображений
        url = f"https://images.wbstatic.net/c{millions}{thousands}/{product_id}/images/big/{i}.jpg"
        image_urls.append(url)

    return image_urls


def download_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        return img
    else:
        return None


# Пример использования:
product_id = 207770067  # ID товара
image_urls = get_images(product_id)

for url in image_urls:
    img = download_image(url)
    if img:
        img.show()  # или сохранить изображение img.save('image.jpg')
    else:
        print(f"Image not found at {url}")

