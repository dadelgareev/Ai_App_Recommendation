import glob
import os
import time

import numpy as np
import psycopg2
import csv
from scipy.spatial.distance import cosine

from transliterate import translit

# Настройки подключения к базе данных
DB_CONFIG = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': 5432
}

# Имя файла CSV
CSV_FILE = 'man_clothes-accs-mujskie-sredstva-i-aksessuary-dlya-odejdy_temp.csv'

# Название таблицы в базе данных
TABLE_NAME = 'products'


# Функция для подключения к PostgreSQL
def connect_to_db():
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        print("Подключение к базе данных установлено.")
        return connection
    except Exception as e:
        print(f"Ошибка подключения к базе данных: {e}")
        exit()


# Функция для вставки данных в таблицу
def insert_data_from_csv(connection, csv_file):
    try:
        cursor = connection.cursor()

        # Чтение данных из CSV
        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            fieldnames = reader.fieldnames

            # Определяем индекс "Бренд"
            brand_index = fieldnames.index('Бренд')

            for row in reader:
                # Подготовка SQL-запроса
                sql = f"""
                INSERT INTO {TABLE_NAME} 
                (source, link, article, vector_representation, price, brand, tags, category) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                # Сбор тегов: все поля, следующие за "Бренд"
                tags = [
                    row[field] for field in fieldnames[brand_index + 1:] if row[field]
                ]

                # Преобразование данных
                data = (
                    row.get('Источник'),
                    row.get('image_url'),
                    row.get('id'),
                    row.get('embedding'),
                    int(row.get('Цена').replace(' ','')) if row.get('Цена') else None,
                    row.get('Бренд'),
                    tags if tags else None,  # Если список тегов пуст, записываем NULL
                    row.get('Категория')
                )

                # Выполнение SQL-запроса
                cursor.execute(sql, data)

        # Сохранение изменений
        connection.commit()
        print("Данные успешно добавлены в таблицу.")
    except Exception as e:
        print(f"Ошибка при добавлении данных: {e}")
        connection.rollback()
    finally:
        cursor.close()


def preview_csv(file_path):
    """
    Выводит заголовки и первые 10 строк из CSV-файла.

    :param file_path: Путь к CSV-файлу
    """
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            # Вывод заголовков
            print("Заголовки CSV (fieldnames):")
            print(reader.fieldnames)
            print()

            # Вывод первых 10 строк
            print("Первые 10 строк:")
            for i, row in enumerate(reader):
                print(row)
                if i >= 9:  # Останавливаемся на 10 строке
                    break
    except Exception as e:
        print(f"Ошибка при чтении CSV: {e}")


def process_all_temp_csv_files():
    # Ищем все файлы с подстрокой '_temp' в имени в текущем проекте
    csv_files = glob.glob(os.path.join(os.getcwd(), '**', '*_temp*.csv'), recursive=True)

    if not csv_files:
        print("Файлы с подстрокой '_temp' не найдены.")
        return

    print(f"Найдены файлы: {csv_files}")
    connection = connect_to_db()

    try:
        for csv_file in csv_files:
            print(f"Обработка файла: {csv_file}")
            insert_data_from_csv(connection, csv_file)
    finally:
        connection.close()
        print("Подключение к базе данных закрыто.")


def create_subtables_with_transliteration(connection):
    try:
        cursor = connection.cursor()

        # 1. Получить уникальные категории
        cursor.execute("SELECT DISTINCT category FROM products")
        categories = cursor.fetchall()
        print(categories)
        for category in categories:
            category_name = category[0]

            # 2. Транслитерировать имя категории
            category_english = translit(category_name, language_code='ru', reversed=True)

            # 3. Преобразовать имя в валидный формат (заменить пробелы и спецсимволы)
            category_english = category_english.replace(' ', '_').lower()

            # 4. Динамически создать таблицу
            sql_create = f"""
            CREATE TABLE IF NOT EXISTS "{category_english}_products" AS
            SELECT * FROM products WHERE category = %s
            """
            cursor.execute(sql_create, (category_name,))
            print(f'{category_english} - таблица создана')

        connection.commit()
        print("Подтаблицы успешно созданы с английскими именами категорий!")
    except Exception as e:
        print("Ошибка:", e)
    finally:
        cursor.close()


def get_vector_from_db(cursor, table_name, item_id):
    # Извлекаем вектор из базы данных как строку
    cursor.execute(f"SELECT vector_representation FROM {table_name} WHERE id = %s", (item_id,))
    result = cursor.fetchone()

    if result:
        # Преобразуем строку в массив чисел (разделитель пробел или запятая)
        vector_str = result[0]  # Получаем строку
        vector = np.array([float(x) for x in vector_str.split(',')])  # Преобразуем строку в массив чисел
        return vector
    return None


def find_similar_items(connection, table_name, item_id, limit=5):
    try:
        cursor = connection.cursor()

        # 1. Получаем вектор для заданного товара
        target_vector = get_vector_from_db(cursor, table_name, item_id)

        if target_vector is None:
            print("Товар с таким ID не найден.")
            return []

        # 2. Извлекаем все векторы из базы данных для поиска похожих
        cursor.execute(f"SELECT id, vector_representation FROM {table_name} WHERE id != %s", (item_id,))
        rows = cursor.fetchall()

        similarities = []

        # 3. Для каждого товара в базе считаем косинусное сходство
        for row in rows:
            item_id_in_db = row[0]
            vector_str = row[1]
            vector = np.array([float(x) for x in vector_str.split(',')])  # Преобразуем строку в массив чисел

            # Косинусное сходство
            similarity = 1 - cosine(target_vector, vector)  # Чем выше, тем более похожи вектора
            similarities.append((item_id_in_db, similarity))

        # Сортируем по схожести и выбираем top-N
        similarities.sort(key=lambda x: x[1], reverse=True)

        # Возвращаем ID товаров с наибольшим сходством
        similar_items = [item[0] for item in similarities[:limit]]
        return similar_items

    except Exception as e:
        print("Ошибка:", e)
        return []
    finally:
        cursor.close()


import time
import numpy as np
from scipy.spatial.distance import cosine


def find_similar_item(connection, table_name, item_id, similarity_threshold=0.90):
    try:
        start_time = time.time()  # Засекаем время начала выполнения функции

        cursor = connection.cursor()

        # 1. Получаем вектор для заданного товара
        vector_start_time = time.time()  # Засекаем время на получение вектора
        target_vector = get_vector_from_db(cursor, table_name, item_id)
        vector_end_time = time.time()

        if target_vector is None:
            print("Товар с таким ID не найден.")
            return None

        print(f"Время получения вектора для товара {item_id}: {vector_end_time - vector_start_time:.4f} сек")

        # 2. Извлекаем все векторы из базы данных для поиска похожих
        query_start_time = time.time()  # Засекаем время выполнения запроса
        cursor.execute(f"SELECT id, vector_representation FROM {table_name} WHERE id != %s", (item_id,))
        rows = cursor.fetchall()
        query_end_time = time.time()

        print(f"Время выполнения SQL-запроса: {query_end_time - query_start_time:.4f} сек")

        # 3. Преобразуем все векторы из базы в массивы заранее
        preprocessing_start_time = time.time()  # Засекаем время на предварительную обработку
        vectors = [(row[0], np.array([float(x) for x in row[1].split(',')])) for row in
                   rows]  # Преобразуем все строки в массивы
        preprocessing_end_time = time.time()

        print(
            f"Время на предварительное преобразование всех векторов: {preprocessing_end_time - preprocessing_start_time:.4f} сек")

        # 4. Для каждого товара в базе считаем косинусное сходство
        loop_start_time = time.time()  # Засекаем время начала перебора
        for item_id_in_db, vector in vectors:
            # Косинусное сходство
            similarity = 1 - cosine(target_vector, vector)  # Чем выше, тем более похожи вектора

            # Если схожесть выше порога, возвращаем этот товар
            if similarity >= similarity_threshold:
                loop_end_time = time.time()
                print(f"Время перебора всех товаров: {loop_end_time - loop_start_time:.4f} сек")
                print(f"Найдено похожее изображение с товаром {item_id_in_db} с сходством {similarity * 100:.2f}%")
                return item_id_in_db

        loop_end_time = time.time()
        print(f"Время перебора всех товаров: {loop_end_time - loop_start_time:.4f} сек")

        print("Похожее изображение не найдено.")
        return None

    except Exception as e:
        print("Ошибка:", e)
        return None
    finally:
        cursor.close()
        end_time = time.time()
        print(f"Общее время выполнения функции: {end_time - start_time:.4f} сек")


# Основная функция
def main():
    #preview_csv("man_clothes-accs-mujskie-sredstva-i-aksessuary-dlya-odejdy_temp.csv")
    connection = connect_to_db()
    #insert_data_from_csv(connection, CSV_FILE)
    #connection.close()
    #process_all_temp_csv_files()
    #create_subtables_with_transliteration(connection)
    #connection.close()
    time_start = time.time()
    item_id = 273475  # ID товара, для которого ищем похожие
    #similar_ids = find_similar_items(connection, "jubki_products", item_id, limit=1)
    result = find_similar_item(connection, "jubki_products", item_id, similarity_threshold=0.85)

    print("Похожие товары:", result)
    time_end = time.time() - time_start
    print(time_end)

if __name__ == '__main__':
    main()
