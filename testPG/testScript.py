from ImageEmbeddingClient import ImageEmbeddingClient
from clientCSV import CsvUploaderClient
from scraper import LamodaScraper
import concurrent.futures

scraper = LamodaScraper()
"""
print(scraper.tags)

scraper.populate_actual_categories()
print(scraper.actual_categories)

scraper.combine_category_data()
print(scraper.combined_data)
"""


grpc_client_AI = ImageEmbeddingClient(server_address="localhost:50052")
grpc_client_CSV = CsvUploaderClient(server_address="localhost:50051")

def process_category(scraper, main_category, category_info):
    href_list = []

    category_name = category_info.get("category_name", 'Не указано')
    category_url = category_info.get("category_url", 'Не указано')
    item_count = category_info.get("item_count", 'Не указано')

    category_short_url = category_url.split('/')[3]
    subcategory = f'{main_category}-{category_short_url}'
    scraper.base_url = 'https://www.lamoda.ru' + category_url

    # Загружаем ссылки для первой страницы
    for j in range(1, 2):
        scraper.get_href_list(j, href_list)
        print(f"Категория - {category_name}, {j} - страничка была загружена")

    # Проверка на дубликаты
    duplicates = scraper.find_duplicates(href_list)
    if duplicates:
        print(f"Дубликаты найдены: {len(duplicates)} - кол-во дубликатов")
        href_list = scraper.remove_duplicates(href_list)
    else:
        print(f"Дубликаты не найдены")

    # Обновляем файл ссылок и CSV для новых ссылок
    scraper.update_links_file_json(f'{subcategory}.json',href_list)
    scraper.create_and_append_csv_json(f'{subcategory}.json',f'{subcategory}.csv',main_category, grpc_client_AI)
    #grpc_client_CSV.upload_csv(f'{subcategory}.csv')


with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = []
    for main_category in scraper.list_categories:
        categories_list = scraper.get_full_width_elements(scraper.list_categories[main_category])
        for category_info in categories_list:
            futures.append(executor.submit(process_category, scraper, main_category, category_info))

    for future in concurrent.futures.as_completed(futures):
        print(f"Категория обработана с результатом: {future.result()}")

"""
categories_list = scraper.get_full_width_elements(scraper.list_categories["women_clothes"])
for i in range(1, 2):
    href_list = list()

    category_name = categories_list[i].get("category_name", 'Не указано')
    category_url = categories_list[i].get("category_url", 'Не указано')
    item_count = categories_list[i].get("item_count", 'Не указано')

    category_short_url = category_url.split('/')[3]
    subcategory = f'{"women_clothes"}-{category_short_url}'
    scraper.base_url = 'https://www.lamoda.ru' + category_url
    for j in range(1, 2):
        scraper.get_href_list(j, href_list)
        print(f"Категория - {category_name}, {j} - страничка была загружена")

    dublicates = scraper.find_duplicates(href_list)
    if dublicates:
        print(f"Дубликаты найдены: {len(dublicates)} - кол-во дубликатов")
        href_list = scraper.remove_duplicates(href_list)
    else:
        print(f"Дубликаты не нйдены")

    new_files = scraper.update_links_file_json(f'{subcategory}.json',href_list)
    scraper.create_and_append_csv_json(f'{subcategory}.json',f'{subcategory}.csv',"women_clothes", grpc_client_AI)
"""
"""
categories_list = scraper.get_full_width_elements(scraper.list_categories["women_clothes"])

# Создаём gRPC-клиент
grpc_client = ImageEmbeddingClient(server_address="localhost:50051")

for i in range(1, 2):  # Перебор категорий
    href_list = list()

    # Извлекаем данные о категории
    category_name = categories_list[i].get("category_name", 'Не указано')
    category_url = categories_list[i].get("category_url", 'Не указано')
    item_count = categories_list[i].get("item_count", 'Не указано')

    # Формируем имя подкатегории и базовый URL
    category_short_url = category_url.split('/')[3]
    subcategory = f'{"women_clothes"}-{category_short_url}'
    scraper.base_url = 'https://www.lamoda.ru' + category_url

    # Сбор ссылок на товары
    for j in range(2, 4):  # Перебор страниц
        scraper.get_href_list(j, href_list)
        print(f"Категория - {category_name}, {j} - страничка была загружена")

    # Проверка на дубликаты
    dublicates = scraper.find_duplicates(href_list)
    if dublicates:
        print(f"Дубликаты найдены: {len(dublicates)} - кол-во дубликатов")
        href_list = scraper.remove_duplicates(href_list)
    else:
        print(f"Дубликаты не найдены")

    # Обновление текстового файла с ссылками
    new_files = scraper.update_links_file_txt(f'{subcategory}.txt', href_list)

    # Создание CSV с вызовом микросервиса
    scraper.create_and_append_csv(new_files, f'{subcategory}.csv', "women_clothes", grpc_client)
"""