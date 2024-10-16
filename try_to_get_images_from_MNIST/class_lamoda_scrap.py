import os
import re
import requests
from bs4 import BeautifulSoup

class LamodaScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
        }

        self.list_categories = {
            "man_shoes": "https://www.lamoda.ru/c/17/shoes-men/?sitelink=topmenuM&l=4",
            "women_shoes": "https://www.lamoda.ru/c/15/shoes-women/?sitelink=topmenuW&l=4",
            "man_clothes": "https://www.lamoda.ru/c/477/clothes-muzhskaya-odezhda/?sitelink=topmenuM&l=3",
            "women_clothes": "https://www.lamoda.ru/c/355/clothes-zhenskaya-odezhda/?sitelink=topmenuW&l=3"
        }

        self.list_urls = []

    def fetch_page(self, page_number=1):
        # Формируем URL с номером страницы
        url = f"{self.base_url}&page={page_number}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Ошибка при выполнении запроса: {response.status_code}")
            return None

    def parse_nuxt_data(self, html):
        # Парсим страницу и ищем скрипт __NUXT__
        soup = BeautifulSoup(html, 'html.parser')
        script_tag = soup.find('script', string=re.compile(r'var __NUXT__'))

        if script_tag:
            script_content = script_tag.string

            # Поиск блока "products" и "settings"
            matches_start = script_content.find('"products"')
            matched_end = script_content.find('settings')

            if matches_start != -1 and matched_end != -1:
                extracted_text = script_content[matches_start:matched_end]
                return extracted_text
        return None

    def extract_page_count(self, extracted_text):
        # Извлекаем количество страниц
        start_index = extracted_text.find('"pages":')
        if start_index != -1:
            text_after_pages = extracted_text[start_index + len('"pages":'):]
            pages_id = text_after_pages.split(',')[0].strip()
            return int(pages_id)
        return None

    def extract_product_data(self, html, extracted_text):
        soup = BeautifulSoup(html, 'html.parser')
        grid_catalog = soup.find('div', class_='grid__catalog')

        if grid_catalog:
            product_cards = grid_catalog.find_all('div', class_='x-product-card__card')

            for number, product_card in enumerate(product_cards, 1):
                product_link = product_card.find('a', class_='x-product-card__link')
                product_url = product_link.get('href', 'URL не найден') if product_link else 'URL не найден'
                product_id = product_url.split('/')[2]
                product_id_upper = product_id.upper() + "_"

                matching_pics = [pic for pic in extracted_text.split('"')
                                 if product_id_upper in pic and (pic.endswith('.jpg') or pic.endswith('.jpeg'))]

                for i in range(len(matching_pics)):
                    matching_pics[i] = "https://a.lmcdn.ru/img236x341" + matching_pics[i]

                product_image = product_card.find('img', class_='x-product-card__pic-img')
                image_src = product_image.get('data-src', product_image.get('src', 'Изображение не найден')) if product_image else 'Изображение не найден'

                price_new = product_card.find('span', class_='x-product-card-description__price-new')
                price_new = price_new.text.strip() if price_new else 'Цена не найдена'

                price_old = product_card.find('span', class_='x-product-card-description__price-old')
                price_old = price_old.text.strip() if price_old else 'Старая цена не найдена'

                product_name = product_card.find('div', class_='x-product-card-description__product-name')
                product_name = product_name.text.strip() if product_name else 'Имя не найдено'

                # Выводим данные товара
                print(f'Номер: {number}')
                print(f'Ссылка на товар: {product_url}')
                print(f'ID продукта: {product_id}')
                print(f'Изображение: {image_src}')
                print(f'Имя продукта: {product_name}')
                print(f'Новая цена: {price_new}')
                print(f'Старая цена: {price_old}')
                print(f'Изображения: {matching_pics}')
                print('-' * 40)

    def scrape_page(self, page_number=1):
        # Получаем HTML страницы
        html = self.fetch_page(page_number)
        if html:
            # Извлекаем текст переменной __NUXT__
            extracted_text = self.parse_nuxt_data(html)

            if extracted_text:
                # Извлекаем количество страниц
                pages_id = self.extract_page_count(extracted_text)
                print(f"Количество страниц: {pages_id}")

                # Извлекаем данные продуктов
                self.extract_product_data(html, extracted_text)
            else:
                print("Не удалось найти данные __NUXT__.")

    def parse_count_pages(self):
        extracted_text = self.fetch_page(self)
        # Находим значение "pages" и извлекаем его
        start_index = extracted_text.find('"pages":')
        if start_index != -1:
            text_after_pages = extracted_text[start_index + len('"pages":'):]
            pages_id = text_after_pages.split(',')[0].strip()
            return pages_id

    def get_image_urls(self, page_number=1):
        # Получаем HTML страницы
        html = self.fetch_page(page_number)
        if html:
            # Извлекаем текст переменной __NUXT__
            extracted_text = self.parse_nuxt_data(html)

            if extracted_text:
                # Разбиваем строку для поиска картинок
                extracted_text = extracted_text.split('"')
                #image_urls = []

                # Находим контейнер с товарами
                grid_catalog = BeautifulSoup(html, 'html.parser').find('div', class_='grid__catalog')

                if grid_catalog:
                    product_cards = grid_catalog.find_all('div', class_='x-product-card__card')

                    for product_card in product_cards:
                        product_id = product_card.find('a', class_='x-product-card__link').get('href', '').split('/')[2]
                        product_id_upper = product_id.upper() + "_"

                        # Извлекаем URL изображений
                        matching_pics = [pic for pic in extracted_text if product_id_upper in pic and (pic.endswith('.jpg') or pic.endswith('.jpeg'))]
                        for pic in matching_pics:
                            self.list_urls.append("https://a.lmcdn.ru/img236x341" + pic)

                return self.list_urls  # Возвращаем список URL изображений
            else:
                print("Не удалось найти данные __NUXT__.")
                return []

    def download_images(self, save_directory):
        # Проверяем, существует ли директория для сохранения, если нет — создаём её
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

        for url in self.list_urls:
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    # Извлекаем имя файла из URL
                    filename = os.path.join(save_directory, url.split('/')[-1])
                    with open(filename, 'wb') as f:
                        f.write(response.content)  # Сохраняем изображение
                    print(f"Скачано: {filename}")
                else:
                    print(f"Ошибка при скачивании {url}: {response.status_code}")
            except Exception as e:
                print(f"Произошла ошибка при скачивании {url}: {e}")



# Использование класса
url = 'https://www.lamoda.ru/c/17/shoes-men/?sitelink=topmenuM&l=4'
scraper = LamodaScraper(url)

# Скрапинг первой страницы
#scraper.scrape_page(1)

# Скрапинг второй страницы
#scraper.scrape_page(2)

print(scraper.parse_count_pages())

url_links = scraper.get_image_urls(1)
print(url_links)

scraper.download_images('images-firts-page')

