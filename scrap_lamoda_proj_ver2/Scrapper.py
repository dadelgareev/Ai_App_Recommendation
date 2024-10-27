import os
import re
import requests
import csv
from bs4 import BeautifulSoup
from collections import Counter

class LamodaScraper:
    def __init__(self, base_url = None):
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

    def get_catalog_href(self,page_number=1):
        text = self.fetch_page(page_number)

        # Разбираем HTML-код страницы с помощью BeautifulSoup
        soup = BeautifulSoup(text, 'html.parser')

        # Находим все элементы <a> с классом x-footer-seo-menu-tab-links__item
        links = soup.find_all('a', class_='x-footer-seo-menu-tab-links__item')

        clothing_data = []
        if links:
            # Проходим по всем найденным элементам и добавляем их в список словарей
            for link in links:
                href = link.get('href')  # Получаем значение атрибута href
                if (href.find('/c/')) == -1: continue #/c/ только каталоги, все остльные домены это всякая залупа по типу брендов и т.д.
                clothing_type = link.get_text(strip=True)  # Получаем текст ссылки (тип одежды)

                # Добавляем словарь с href и типом одежды в список
                clothing_data.append({'href': href, 'type': clothing_type})

            return clothing_data  # Возвращаем список словарей
        else:
            print("Элемент с классом 'x-footer-seo-menu-tabs' не найден.")

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

    def extract_page_count(self, extracted_text):
        # Извлекаем количество страниц
        start_index = extracted_text.find('"pages":')
        if start_index != -1:
            text_after_pages = extracted_text[start_index + len('"pages":'):]
            pages_id = text_after_pages.split(',')[0].strip()
            return int(pages_id)
        return None

    def extract_product_data_for_cvs(self,html,extracted_text, data_set):
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

                if not (matching_pics): ["Изображения не найдены"]
                else:
                    for i in range(len(matching_pics)):
                        matching_pics[i] = "https://a.lmcdn.ru/img236x341" + matching_pics[i]

                product_image = product_card.find('img', class_='x-product-card__pic-img')
                image_src = product_image.get('data-src', product_image.get('src','Изображение не найден')) if product_image else 'Изображение не найден'

                price_new = product_card.find('span', class_='x-product-card-description__price-new')
                price_new = price_new.text.strip() if price_new else 'Цена не найдена'

                price_old = product_card.find('span', class_='x-product-card-description__price-old')
                price_old = price_old.text.strip() if price_old else 'Старая цена не найдена'

                product_name = product_card.find('div', class_='x-product-card-description__product-name')
                product_name = product_name.text.strip() if product_name else 'Имя не найдено'


                # Добавляем данные в словарь
                data_set["product_id"].append(product_id)
                data_set["product_url"].append(product_url)
                data_set["product_name"].append(product_name)
                data_set["image_url"].append(image_src)
                data_set["price_new"].append(price_new)
                data_set["price_old"].append(price_old)
                data_set["matching_pics"].append(matching_pics)
    def print_product_data(self, html, extracted_text):
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

    def create_data_set_csv(self):
        pass

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
                self.print_product_data(html, extracted_text)
            else:
                print("Не удалось найти данные __NUXT__.")

    def parse_count_pages(self):
        extracted_text = self.fetch_page()
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
                image_urls = []

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
                            image_urls.append("https://a.lmcdn.ru/img236x341" + pic)
                print(f"Url с данной страницы: {page_number} сохрнены в список" )
                return image_urls  # Возвращаем список URL изображений
            else:
                print("Не удалось найти данные __NUXT__.")
                return []

    def download_images(self, save_directory, image_urls):
        # Проверяем, существует ли директория для сохранения, если нет — создаём её
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

        for url in image_urls:
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

    def get_categories(self):
        print(self.list_categories)

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

    def create_csv(self, data, output_file='dataset.csv'):
        # Создаём файл CSV
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            # Пишем заголовки для столбцов
            headers = ['Image Path', 'Category Name', 'Category URL'] + list(data['attributes'].keys())
            writer.writerow(headers)

            # Пробегаемся по каждому изображению и создаём строку с данными
            for image_url in data['image_urls']:
                image_path = os.path.basename(image_url)  # Здесь можно указать путь сохранённых изображений
                for category_name, category_url in data['categories'].items():
                    # Создаем строку для каждой комбинации изображение-категория
                    row = [image_path, category_name, category_url]

                    # Добавляем атрибуты к строке
                    for attr_name in data['attributes'].keys():
                        row.append(data['attributes'].get(attr_name, 'N/A'))

                    # Пишем строку в CSV
                    writer.writerow(row)

        print(f"CSV файл успешно создан: {output_file}")

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

    def create_csv_from_txt(self, txt_file, output_csv):
        # Открываем файл с URL и создаем CSV-файл
        with open(txt_file, 'r') as file, open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            # Настраиваем заголовки CSV-файла
            fieldnames = ['image_url', 'Сезон', 'Материал подошвы', 'Материал верха', 'Цвет', 'Страна производства']
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

                # Достаём интересующие нас атрибуты
                season = attributes.get('Сезон', 'Не указано')
                sole_material = attributes.get('Материал подошвы', 'Не указано')
                upper_material = attributes.get('Материал верха', 'Не указано')
                color = attributes.get('Цвет', 'Не указано')

                # Проходимся по каждой картинке и записываем данные в CSV
                for image_url in image_urls:
                    writer.writerow({
                        'image_url': image_url,
                        'Сезон': season,
                        'Материал подошвы': sole_material,
                        'Материал верха': upper_material,
                        'Цвет': color
                    })
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
    def create_csv_and_download_images(self, txt_file, output_csv, images_dir):
        """Скачивает изображения и создает CSV с путями и атрибутами."""
        # Создаем директорию для картинок, если её нет
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)
        count = 0
        page = 1
        # Открываем файл с URL и создаем CSV-файл
        with open(txt_file, 'r') as file, open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            # Настраиваем заголовки CSV-файла
            fieldnames = ['image_path', 'Сезон', 'Материал подошвы', 'Материал верха', 'Цвет', 'Категория']
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
                categories = result.get('categories',{})

                # Достаём интересующие нас атрибуты
                season = attributes.get('Сезон', 'Не указано')
                sole_material = attributes.get('Материал подошвы', 'Не указано')
                upper_material = attributes.get('Материал верха', 'Не указано')
                color = attributes.get('Цвет', 'Не указано')
                if categories:
                    category = list(categories.keys())[0]  # Получаем первый ключ
                else: category = 'Не указано'

                count+=1
                if count == 60:
                    print(f"{page} - скачана")
                    count = 0
                    page+= 1

                # Скачиваем и записываем данные для каждой картинки
                for i, image_url in enumerate(image_urls):
                    image_name = f'image_{i}_{os.path.basename(image_url)}'
                    image_path = self.download_image(image_url, images_dir, image_name)

                    if image_path:
                        writer.writerow({
                            'image_path': image_path,
                            'Сезон': season,
                            'Материал подошвы': sole_material,
                            'Материал верха': upper_material,
                            'Цвет': color,
                            'Категория': category
                        })

    def get_full_width_elements(self, url):
        """Находит все элементы с классом 'x-tree-view-catalog-navigation__category' без дополнительных классов"""
        html = self.fetch_page(url)
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

    def update_links_file(self, filename):
        # Загрузка ссылок из существующего файла, если он есть
        if os.path.exists(filename):
            with open(filename, "r") as file:
                self.current_links = set(line.strip() for line in file)

        # Парсим новые ссылки
        parsed_links = set(self.get_href_list())

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