import os
import re
import requests
import csv
from bs4 import BeautifulSoup
from collections import Counter

class LamodaScraper:
    def __init__(self):
        self.list_categories = {
            "man_shoes": "https://www.lamoda.ru/c/17/shoes-men/?sitelink=topmenuM&l=4",
            "women_shoes": "https://www.lamoda.ru/c/15/shoes-women/?sitelink=topmenuW&l=4",
            "man_clothes": "https://www.lamoda.ru/c/477/clothes-muzhskaya-odezhda/?sitelink=topmenuM&l=3",
            "women_clothes": "https://www.lamoda.ru/c/355/clothes-zhenskaya-odezhda/?sitelink=topmenuW&l=3"
        }
        self.tags = {
            "man_shoes": ['Сезон','Материал подошвы','Материал верха','Цвет'],
            "women_shoes": ['Сезон','Материал подошвы','Материал верха','Цвет'],
            "man_clothes": ['Сезон', 'Цвет', 'Узор', 'Фасон'],
            "women_clothes": ['Сезон', 'Цвет', 'Узор', 'Фасон']
        }
        self.base_url = self.list_categories["man_shoes"]
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
        }
        self.actual_categories = []

    def fetch_page(self, page_number=1, custom_url=None):
        # Если передан custom_url, используем его, иначе формируем URL с номером страницы
        if custom_url is not None:
            url = custom_url
        else:
            # Формируем URL с номером страницы
            url = f"{self.base_url}?page={page_number}"


        # Выполняем запрос к указанному URL
        response = requests.get(url, headers=self.headers)

        # Если запрос выполнен успешно (код 200), возвращаем текст страницы
        if response.status_code == 200:
            return response.text
        else:
            print(f"Ошибка при выполнении запроса: {response.status_code}")
            return None

    def parse_count_pages(self):
        extracted_text = self.fetch_page()
        # Находим значение "pages" и извлекаем его
        start_index = extracted_text.find('"pages":')
        if start_index != -1:
            text_after_pages = extracted_text[start_index + len('"pages":'):]
            pages_id = text_after_pages.split(',')[0].strip()
            return pages_id

    def get_all_atrib_from_page(self, url):
        # Получаем HTML страницы
        html = self.fetch_page(1, url)

        # Парсим HTML с помощью BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Находим все теги img с классом 'x-premium-product-gallery__image'
        gallery_images = soup.find_all('img', class_='x-premium-product-gallery__image')

        image_urls = []

        # Извлекаем значения 'src' и добавляем префикс https:
        for img in gallery_images:
            src = img.get('src')
            if src:
                # Добавляем к ссылке https если её нет
                full_url = f"https:{src}"
                image_urls.append(full_url)

        # Находим блок с описанием категорий
        categories_value = {}
        category_elements = soup.find_all('div', class_='x-breadcrumbs__slide')

        element = category_elements[len(category_elements)-1]
        link = element.find('a')
        if link:
            category_name = link.get_text(strip=True)
            category_url = link.get('href')
            categories_value[category_name] = category_url

        # Находим блок с описанием атрибутов
        attributes_section = soup.find('div', class_='x-premium-product-page__description')

        attributes = {}

        if attributes_section:
            # Находим все элементы, содержащие атрибуты продукта
            attribute_items = attributes_section.find_all('p', class_='x-premium-product-description-attribute')

            # Проходимся по каждому элементу и извлекаем название и значение
            for item in attribute_items:
                name = item.find('span', class_='x-premium-product-description-attribute__name').text.strip()
                value = item.find('span', class_='x-premium-product-description-attribute__value').text.strip()
                attributes[name] = value
        #print(soup)
        # Возвращаем изображения, атрибуты и категории
        return {
            "image_urls": image_urls,
            "attributes": attributes,
            "categories": categories_value
        }

    def get_full_width_elements(self, url):
        """Находит все элементы с классом 'x-tree-view-catalog-navigation__category' без дополнительных классов"""
        html = self.fetch_page(1, url)
        if html:
            soup = BeautifulSoup(html, 'html.parser')

            # Находим все элементы с классом 'x-tree-view-catalog-navigation__category'
            category_elements = soup.find_all('div', class_='x-tree-view-catalog-navigation__category')

            categories_info = []
            for element in category_elements:
                # Проверяем, что элемент содержит только класс 'x-tree-view-catalog-navigation__category'
                if element.get('class') == ['x-tree-view-catalog-navigation__category']:
                    # Извлекаем ссылку на категорию
                    link = element.find('a', class_='x-link')
                    # Извлекаем количество товаров
                    count = element.find('span', class_='x-tree-view-catalog-navigation__found')

                    if link and count:
                        category_name = link.text.strip()  # Название категории
                        category_url = link['href']  # Ссылка на категорию
                        item_count = count.text.strip()  # Количество товаров

                        # Сохраняем информацию в список
                        categories_info.append({
                            'category_name': category_name,
                            'category_url': category_url,
                            'item_count': item_count
                        })

            return categories_info
        else:
            return []

    def get_href_list(self,page=1, href_list = None):
        # Инициализируем список, если он не передан
        if href_list is None:
            href_list = []

        html = self.fetch_page(page)
        soup = BeautifulSoup(html, 'html.parser')
        grid_catalog = soup.find('div', class_='grid__catalog')

        if grid_catalog:
            product_cards = grid_catalog.find_all('div', class_='x-product-card__card')

            for number, product_card in enumerate(product_cards, 1):
                product_link = product_card.find('a', class_='x-product-card__link')
                product_url = product_link.get('href', 'URL не найден') if product_link else 'URL не найден'

                href_list.append("https://www.lamoda.ru/" + product_url)
        return href_list

    def save_links_to_txt(self, links, output_file='links.txt'):
        # Открываем файл для записи
        with open(output_file, mode='w', encoding='utf-8') as file:
            # Проходим по списку ссылок и записываем каждую ссылку на новой строке
            for link in links:
                file.write(f"{link}\n")  # Записываем ссылку и перевод строки

        print(f"Ссылки успешно сохранены в файл: {output_file}")

    def find_duplicates(self,all_links):
        link_counts = Counter(all_links)
        duplicates = [link for link, count in link_counts.items() if count > 1]
        return duplicates

    def remove_duplicates(self, all_links):
        # Подсчитываем количество вхождений каждой ссылки
        link_counts = Counter(all_links)

        # Оставляем только уникальные ссылки
        unique_links = [link for link, count in link_counts.items() if count > 0]

        return unique_links

    def download_image(self, url, save_dir, image_name):
        """Скачивает картинку по URL и сохраняет её в указанную директорию."""
        try:
            response = requests.get(url)
            if response.status_code == 200:
                image_path = os.path.join(save_dir, image_name)
                with open(image_path, 'wb') as img_file:
                    img_file.write(response.content)
                return image_path  # Возвращаем путь к скачанной картинке
            else:
                print(f"Ошибка при скачивании изображения: {url}, статус: {response.status_code}")
        except Exception as e:
            print(f"Не удалось скачать изображение: {url}. Ошибка: {e}")
        return None

    def create_csv_and_download_images(self, txt_file, output_csv, images_dir, category_key):
        """Скачивает изображения и создает CSV с путями и атрибутами."""

        # Создаем директорию для картинок, если её нет
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)

        # Получаем список атрибутов для выбранной категории
        selected_tags = list(self.tags[category_key])

        # Поля CSV-файла: путь к картинке, категория, и каждый тег по отдельности
        fieldnames = ['image_path', 'Категория'] + selected_tags

        # Открываем файл с URL и создаем CSV-файл
        with open(txt_file, 'r') as file, open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Записываем заголовки
            writer.writeheader()

            # Проходимся по каждой ссылке в txt-файле
            for url in file:
                url = url.strip()  # Убираем пробелы и переносы строки

                # Вызываем метод для получения атрибутов и картинок
                result = self.get_all_atrib_from_page(url)

                # Берём список URL картинок
                image_urls = result.get('image_urls', [])

                # Берём атрибуты
                attributes = result.get('attributes', {})

                # Берем категории
                categories = result.get('categories', {})

                # Определяем категорию
                category = list(categories.keys())[0] if categories else 'Не указано'

                # Скачиваем и записываем данные для каждой картинки
                for i, image_url in enumerate(image_urls):
                    image_name = f'image_{i}_{os.path.basename(image_url)}'
                    image_path = self.download_image(image_url, images_dir, image_name)

                    # Составляем строку данных с выбранными тегами
                    row_data = {'image_path': image_path, 'Категория': category}
                    for tag in selected_tags:
                        row_data[tag] = attributes.get(tag, 'Не указано')

                    if image_path:
                        writer.writerow(row_data)

    def update_links_file(self, filename, page=1):
        # Загрузка ссылок из существующего файла, если он есть
        if os.path.exists(filename):
            with open(filename, "r") as file:
                self.current_links = set(line.strip() for line in file)

        # Парсим новые ссылки с указанной страницы и URL
        parsed_links = set(self.get_href_list(page=page))

        # Определяем новые ссылки
        new_links = parsed_links - self.current_links

        # Если есть новые ссылки, добавляем их и обновляем файл
        if new_links:
            with open(filename, "a") as file:
                for link in new_links:
                    file.write(link + "\n")
            print(f"{len(new_links)} новых ссылок добавлено.")
        else:
            print("Новых ссылок не найдено.")

    def update_links_file_and_dataset(self, links_filename, dataset_filename, images_dir, page=1,
                                      category="man_shoes"):
        """Обновляет файл ссылок, добавляет новые ссылки и дополняет датасет CSV."""

        # Загружаем существующие ссылки, если файл уже создан
        current_links = set()
        if os.path.exists(links_filename):
            with open(links_filename, "r") as file:
                current_links = set(line.strip() for line in file)

        # Получаем новые ссылки с указанной страницы и URL
        parsed_links = set(self.get_href_list(page=page))
        new_links = parsed_links - current_links  # Определяем новые ссылки

        # Если есть новые ссылки, добавляем их в файл
        if new_links:
            with open(links_filename, "a") as file:
                for link in new_links:
                    file.write(link + "\n")
            print(f"{len(new_links)} новых ссылок добавлено.")
        else:
            print("Новых ссылок не найдено.")
            return

        # Теперь дополняем датасет для новых ссылок
        self.append_to_dataset(new_links, dataset_filename, images_dir, category)

    def append_to_dataset(self, links, dataset_filename, images_dir, category):
        """Дополняет датасет CSV новыми записями для указанных ссылок."""

        # Определяем нужные теги для категории
        tags = [tag.strip() for tag in self.tags.get(category, [])]
        fieldnames = ['image_path', 'Категория'] + tags  # Заголовки CSV: путь, категория, теги

        # Открываем CSV в режиме добавления (append)
        with open(dataset_filename, "a", newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Обходим каждую ссылку
            for url in links:
                result = self.get_all_atrib_from_page(url)  # Получаем данные по ссылке

                # Получаем URL изображений и атрибуты
                image_urls = result.get('image_urls', [])
                attributes = result.get('attributes', {})
                categories = result.get('categories', {})

                # Извлекаем значение категории
                category_name = list(categories.keys())[0] if categories else 'Не указано'

                # Формируем строку для каждого изображения
                for i, image_url in enumerate(image_urls):
                    image_name = f'image_{i}_{os.path.basename(image_url)}'
                    image_path = self.download_image(image_url, images_dir, image_name)

                    # Составляем строку данных: путь к изображению, категория, теги
                    row = {'image_path': image_path, 'Категория': category_name}
                    row.update({tag: attributes.get(tag, 'Не указано') for tag in tags})

                    if image_path:
                        writer.writerow(row)

    def populate_actual_categories(self):
        for main_category_name, main_category_url in self.list_categories.items():
            # Получаем список вложенных категорий
            categories_list = self.get_full_width_elements(main_category_url)

            for category in categories_list:
                # Извлекаем имя и URL категории
                category_url = category.get("category_url", 'Не указано')
                category_short_url = f"{main_category_name}-{category_url.split('/')[3]}"
                print(category_short_url)
                # Добавляем категорию в словарь с именем как ключ, URL как значение
                self.actual_categories.append(category_short_url)

    def read_tags_from_csv(self, category_name, base_dir="categories"):
        """
        Читает данные из CSV файла в соответствующей директории категории.
        :param category_name: Название категории, CSV для которой нужно прочитать.
        :param base_dir: Базовая директория для хранения категорий.
        :return: Список словарей с полями 'image_path' и 'tags'.
        """
        # Путь к директории категории и CSV-файлу
        category_dir = os.path.join(base_dir, category_name)
        csv_path = os.path.join(category_dir, f"{category_name}.csv")

        # Проверка наличия CSV файла
        if not os.path.exists(csv_path):
            print(f"CSV файл не найден для категории: {category_name}")
            return []

        # Чтение CSV файла
        tags_data = []
        with open(csv_path, mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                tags_data.append({
                    "image_path": row["image_path"],
                    "tags": row["tags"].split(", ")  # Разбиваем теги на список
                })

        return tags_data