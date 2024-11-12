import os
import re
import requests
import csv
from bs4 import BeautifulSoup
from collections import Counter
from transformerG import ImageEmbeddingProcessor

class LamodaScraper:
    def __init__(self):
        self.list_categories = {
            "man_shoes": "https://www.lamoda.ru/c/17/shoes-men/?sitelink=topmenuM&l=4",
            "women_shoes": "https://www.lamoda.ru/c/15/shoes-women/?sitelink=topmenuW&l=4",
            "man_clothes": "https://www.lamoda.ru/c/477/clothes-muzhskaya-odezhda/?sitelink=topmenuM&l=3",
            "women_clothes": "https://www.lamoda.ru/c/355/clothes-zhenskaya-odezhda/?sitelink=topmenuW&l=3"
        }
        self.tags = {
            "man_shoes": ['Сезон','Материал подошвы','Материал верха','Цвет', 'Внутренний материал', 'Материал подошвы', 'Рисунок', 'Тип носа','Застежка'],
            "women_shoes": ['Сезон','Материал подошвы','Материал верха','Цвет', 'Внутренний материал', 'Материал подошвы', 'Рисунок', 'Тип носа','Застежка'],
            "man_clothes": ['Сезон', 'Цвет', 'Узор', 'Фасон','Тип ткани', 'Посадка', 'Застежка', 'Детали','Флисовая подкладка', 'Внешние карманы', 'Материал подкладки, %','Состав, %'],
            "women_clothes": ['Сезон', 'Цвет', 'Узор', 'Фасон','Тип ткани', 'Посадка', 'Застежка', 'Детали','Флисовая подкладка', 'Внешние карманы', 'Материал подкладки, %','Состав, %']
        }
        self.base_url = self.list_categories["man_shoes"]
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
        }
        self.actual_categories = {}

        self.combined_data = []
        self.model = ImageEmbeddingProcessor()

    def fetch_page(self, page_number=1, custom_url=None):
        # Если передан custom_url, используем его, иначе формируем URL с номером страницы
        if custom_url is not None:
            url = custom_url
        elif page_number == 1 and custom_url is not None:
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

    def populate_actual_categories(self):
        self.actual_categories = {}  # Инициализируем словарь

        for main_category_name, main_category_url in self.list_categories.items():
            # Получаем список вложенных категорий
            categories_list = self.get_full_width_elements(main_category_url)

            # Инициализируем список категорий для основного ключа
            self.actual_categories[main_category_name] = []

            for category in categories_list:
                # Извлекаем имя и URL категории
                category_url = category.get("category_url", 'Не указано')
                category_short_url = f"{main_category_name}-{category_url.split('/')[3]}"

                # Добавляем категорию в список для основного ключа
                self.actual_categories[main_category_name].append(category_short_url)

    def read_tags_from_csv(self, category_name, base_dir=""):
        """
        Читает данные из CSV файла в соответствующей директории категории.
        :param category_name: Название категории, CSV для которой нужно прочитать.
        :param base_dir: Базовая директория для хранения категорий.
                         Если не указана, файл ищется в корневой директории проекта.
        :return: Список строк из CSV файла (после заголовка), каждая строка - одна цельная строка.
        """
        # Проверка и добавление расширения .csv, если его нет в названии категории
        if not category_name.endswith('.csv'):
            category_name += ".csv"

        # Определение полного пути к CSV-файлу
        csv_path = os.path.join(base_dir, category_name) if base_dir else category_name

        # Проверка наличия CSV файла
        if not os.path.exists(csv_path):
            print(f"CSV файл не найден для категории: {category_name}")
            return []

        # Чтение CSV файла
        data_rows = []
        with open(csv_path, mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)

            # Пропускаем заголовок и добавляем все строки после него
            next(reader)  # Пропускаем первую строку (заголовок)
            for row in reader:
                data_rows.append(", ".join(row))  # Объединяем элементы строки в одну строку

        return data_rows


    def combine_category_data(self):
        self.combined_data = []
        for main_category, subcategories in self.actual_categories.items():
            tags = self.tags.get(main_category, [])  # Получаем теги для категории или пустой список
            for subcategory in subcategories:
                self.combined_data.append([main_category, subcategory, ','.join(tags)])
        return self.combined_data

    def create_csv(self, new_links, output_csv, category_key):
        """Добавляет новые ссылки в существующий CSV-файл с категориями, тегами, нормой эмбеддинга и источником."""

        new_tags = []
        selected_tags = list(self.tags[category_key])  # Получаем список атрибутов для выбранной категории

        # Поля CSV-файла: ссылка на картинку, ID, категория, норма эмбеддинга, источник и теги
        fieldnames = ['image_url', 'id', 'Категория', 'embedding_norm', 'Источник'] + selected_tags
        file_exists = os.path.isfile(output_csv)

        # Создание директории для изображений на основе имени CSV-файла (без расширения)
        images_dir = os.path.splitext(output_csv)[0]
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)

        # Открываем CSV-файл в режиме добавления или записи, если файл отсутствует
        with open(output_csv, 'a' if file_exists else 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Записываем заголовки, если файл только что создан
            if not file_exists:
                writer.writeheader()

            # Проходимся по каждой новой ссылке
            for url in new_links:
                url = url.strip()

                try:
                    # Получаем атрибуты и изображения для текущей ссылки
                    result = self.get_all_atrib_from_page(url)
                except Exception as e:
                    print(f"Ошибка при обработке URL {url}: {e}")
                    continue

                # Берём список URL картинок
                image_urls = result.get('image_urls', [])
                attributes = result.get('attributes', {})
                categories = result.get('categories', {})
                category = list(categories.keys())[0] if categories else 'Не указано'

                # Записываем данные для каждой картинки
                for image_url in image_urls:
                    temp_tags = []

                    # Загружаем изображение в директорию и формируем путь к файлу
                    image_name = image_url.split('/')[-1]
                    image_path = os.path.join(images_dir, image_name)
                    if not os.path.exists(image_path):  # Скачиваем только если файла нет
                        self.download_image(image_url, images_dir, image_name)

                    # Получаем вектор эмбеддинга
                    embedding = self.model.get_embedding(image_path)
                    if embedding is not None:
                        # Преобразуем тензор эмбеддинга в список, а затем в строку для записи в CSV
                        embedding_str = ','.join(map(str, embedding.cpu().numpy()))
                    else:
                        embedding_str = 'Ошибка'

                    # Составляем строку данных с выбранными тегами, нормой эмбеддинга и источником
                    row_data = {
                        'image_url': image_url,
                        'id': image_url.split('/')[6].split('_')[0],
                        'Категория': category,
                        'embedding_norm': "None",
                        'Источник': 'Lamoda'
                    }

                    # Добавляем теги для выбранной категории
                    for tag in selected_tags:
                        row_data[tag] = attributes.get(tag, 'Не указано')

                    # Преобразуем tags в строку и добавляем в new_tags
                    temp_tags.extend([image_url, image_url.split('/')[6].split('_')[0], category, embedding_str, 'Lamoda'])
                    for tag in selected_tags:
                        temp_tags.append(attributes.get(tag, 'Не указано'))

                    # Добавляем сформированную строку тегов
                    new_tags.append(','.join(temp_tags))

                    # Записываем строку в CSV
                    writer.writerow(row_data)

        print("Обновление CSV завершено.")
        return new_tags


    def create_and_append_csv(self, new_links, output_csv, category_key):
        """Добавляет новые ссылки в существующий и новый CSV-файлы с категориями, тегами, эмбеддингом и источником."""

        # Создаём имя нового CSV-файла с припиской '_temp'
        temp_output_csv = os.path.splitext(output_csv)[0] + '_temp.csv'
        selected_tags = list(self.tags[category_key])  # Получаем список атрибутов для выбранной категории

        # Поля CSV-файла
        fieldnames = ['image_url', 'id', 'Категория', 'embedding', 'Источник'] + selected_tags

        # Создание директории для изображений, если ещё не существует
        images_dir = os.path.splitext(output_csv)[0]
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)

        # Открываем исходный и новый файлы
        with open(output_csv, 'a', newline='', encoding='utf-8') as old_csvfile, \
                open(temp_output_csv, 'w', newline='', encoding='utf-8') as new_csvfile:

            # Создаем писателей для обоих файлов
            old_writer = csv.DictWriter(old_csvfile, fieldnames=fieldnames)
            new_writer = csv.DictWriter(new_csvfile, fieldnames=fieldnames)

            # Записываем заголовок в новый файл, если только он был создан
            new_writer.writeheader()

            # Проходимся по каждой новой ссылке
            for url in new_links:
                url = url.strip()

                try:
                    result = self.get_all_atrib_from_page(url)  # Получаем атрибуты и изображения для текущей ссылки
                except Exception as e:
                    print(f"Ошибка при обработке URL {url}: {e}")
                    continue

                # Берём список URL картинок
                image_urls = result.get('image_urls', [])
                attributes = result.get('attributes', {})
                categories = result.get('categories', {})
                category = list(categories.keys())[0] if categories else 'Не указано'

                # Записываем данные для каждой картинки
                for image_url in image_urls:
                    # Загружаем изображение в директорию
                    image_name = image_url.split('/')[-1]
                    image_path = os.path.join(images_dir, image_name)
                    if not os.path.exists(image_path):
                        self.download_image(image_url, images_dir, image_name)

                    # Получаем вектор эмбеддинга и преобразуем в строку для записи
                    embedding = self.model.get_embedding(image_path)
                    embedding_str = ','.join(map(str, embedding.cpu().numpy())) if embedding is not None else 'Ошибка'

                    # Составляем строку данных
                    row_data = {
                        'image_url': image_url,
                        'id': image_url.split('/')[6].split('_')[0],
                        'Категория': category,
                        'embedding': "None",
                        'Источник': 'Lamoda'
                    }

                    # Добавляем теги для выбранной категории
                    for tag in selected_tags:
                        row_data[tag] = attributes.get(tag, 'Не указано')

                    # Записываем строку в оба CSV файла
                    old_writer.writerow(row_data)
                    new_writer.writerow(row_data)

        print(f"Данные добавлены в '{output_csv}' и '{temp_output_csv}'")

    def update_links_file_txt(self, filename, parsed_links):
        """
        Обновляет файл ссылок, добавляя новые ссылки, если они отсутствуют в текущем файле.

        :param filename: Имя txt-файла с уже существующими ссылками.
        :param parsed_links: Список новых ссылок, которые нужно проверить и добавить.
        :return: Список новых добавленных ссылок.
        """
        # Преобразуем список ссылок в множество для быстрого поиска и исключаем дубликаты
        parsed_links_set = set(parsed_links)

        # Загружаем существующие ссылки из файла, если файл существует
        current_links = set()
        if os.path.exists(filename):
            with open(filename, "r") as file:
                current_links = set(line.strip() for line in file)

        # Определяем новые ссылки, которых еще нет в текущем файле
        new_links = parsed_links_set - current_links

        # Если есть новые ссылки, добавляем их в файл
        if new_links:
            with open(filename, "a") as file:
                for link in new_links:
                    file.write(link + "\n")
            print(f"{len(new_links)} новых ссылок добавлено.")
        else:
            print("Новых ссылок не найдено.")

        return list(new_links)  # Возвращаем список добавленных ссылок

