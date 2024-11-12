import os
import shutil
import concurrent.futures
import time
import grpc
import scraperCSV_pb2
import scraperCSV_pb2_grpc
from scraper import LamodaScraper


def clean_directory():
    """
    Удаляет все файлы .csv и .txt только в корневой директории проекта.
    Не заходит в подкаталоги.
    """
    # Проходим по файлам только в текущей директории (без рекурсивного обхода)
    for file in os.listdir("."):
        # Получаем полный путь к файлу
        file_path = os.path.join(".", file)

        # Проверяем, что это файл и он имеет расширение .csv или .txt
        if os.path.isfile(file_path) and (file.endswith(".csv") or file.endswith(".txt")):
            try:
                os.remove(file_path)
                print(f"Удален файл: {file_path}")
            except Exception as e:
                print(f"Не удалось удалить файл {file_path}: {e}")


def upload_csv(stub, file_path, file_name):
    # Открываем CSV файл и читаем его содержимое
    with open(file_path, 'rb') as f:
        file_content = f.read()

    # Создаем запрос с содержимым файла и его именем
    request = scraperCSV_pb2.UploadRequest(
        file_content=file_content,
        file_name=file_name
    )

    # Отправляем запрос серверу и получаем ответ
    response = stub.UploadCSV(request)
    print("Ответ сервера:", response.message)


def process_category(scraper, main_category, category_info, stub):
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
        print("Дубликаты не найдены")

    # Обновляем файл ссылок и CSV для новых ссылок
    new_files = scraper.update_links_file_txt(f'{subcategory}.txt', href_list)
    scraper.create_csv(new_files, f'{subcategory}.csv', main_category)
    # Загружаем CSV файл
    upload_csv(stub, f'{subcategory}.csv', f'{subcategory}.csv')
    return f"Обработка категории {category_name} завершена"


def run():
    scraper = LamodaScraper()

    # Создаем один канал и stub для всех потоков
    channel = grpc.insecure_channel('localhost:5000')
    stub = scraperCSV_pb2_grpc.FileTransferStub(channel)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for main_category in scraper.list_categories:
            categories_list = scraper.get_full_width_elements(scraper.list_categories[main_category])
            for category_info in categories_list:
                futures.append(executor.submit(process_category, scraper, main_category, category_info, stub))

        for future in concurrent.futures.as_completed(futures):
            print(f"Категория обработана с результатом: {future.result()}")

if __name__ == '__main__':
    # Очищаем директорию перед запуском основного кода
    clean_directory()

    start_time = time.time()
    run()
    end_time = time.time()
    print("Общее время выполнения:", end_time - start_time)

