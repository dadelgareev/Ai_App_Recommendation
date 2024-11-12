from scraper import LamodaScraper
import concurrent.futures

scraper = LamodaScraper()

print(scraper.tags)

scraper.populate_actual_categories()
print(scraper.actual_categories)

scraper.combine_category_data()
print(scraper.combined_data)


"""
categories_list = scraper.get_full_width_elements(scraper.list_categories["man_shoes"])
href_list = list()

category_name = categories_list[0].get("category_name", 'Не указано')
category_url = categories_list[0].get("category_url", 'Не указано')
item_count = categories_list[0].get("item_count", 'Не указано')

category_short_url = category_url.split('/')[3]
subcategory = f'{"man_shoes"}-{category_short_url}'
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

scraper.save_links_to_txt(href_list, f'{subcategory}.txt')
scraper.create_only_csv(f'{subcategory}.txt',f'{subcategory}.csv',"man_shoes")

scraper.read_tags_from_csv(f'{subcategory}.csv')

new_links = scraper.update_links_file(f'{subcategory}.txt', 1)
scraper.append_to_existing_csv(new_links, f'{subcategory}.csv', "man_shoes")
"""
"""
categories_list = scraper.get_full_width_elements(scraper.list_categories["women_clothes"])
href_list = list()

category_name = categories_list[0].get("category_name", 'Не указано')
category_url = categories_list[0].get("category_url", 'Не указано')
item_count = categories_list[0].get("item_count", 'Не указано')

category_short_url = category_url.split('/')[3]
subcategory = f'{"man_shoes"}-{category_short_url}'
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

scraper.save_links_to_txt(href_list, f'{subcategory}.txt')
scraper.create_only_csv(f'{subcategory}.txt',f'{subcategory}.csv',"women_clothes")

scraper.read_tags_from_csv(f'{subcategory}.csv')

scraper.get_href_list(3, href_list)

new_links = scraper.update_links_file_txt(f'{subcategory}.txt', href_list)
new_tags = scraper.append_to_existing_csv(new_links, f'{subcategory}.csv', "women_clothes")
print(new_tags)
"""
"""
categories_list = scraper.get_full_width_elements(scraper.list_categories["women_clothes"])
for i in range(0, len(categories_list)):
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

    new_files = scraper.update_links_file_txt(f'{subcategory}.txt',href_list)
    scraper.append_to_existing_csv(new_files,f'{subcategory}.csv',"women_clothes")
"""
"""
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
    new_files = scraper.update_links_file_txt(f'{subcategory}.txt', href_list)
    scraper.append_to_existing_csv(new_files, f'{subcategory}.csv', main_category)


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

    new_files = scraper.update_links_file_txt(f'{subcategory}.txt',href_list)
    scraper.create_csv(new_files,f'{subcategory}.csv',"women_clothes")

categories_list = scraper.get_full_width_elements(scraper.list_categories["women_clothes"])
for i in range(1, 2):
    href_list = list()

    category_name = categories_list[i].get("category_name", 'Не указано')
    category_url = categories_list[i].get("category_url", 'Не указано')
    item_count = categories_list[i].get("item_count", 'Не указано')

    category_short_url = category_url.split('/')[3]
    subcategory = f'{"women_clothes"}-{category_short_url}'
    scraper.base_url = 'https://www.lamoda.ru' + category_url
    for j in range(2, 4):
        scraper.get_href_list(j, href_list)
        print(f"Категория - {category_name}, {j} - страничка была загружена")

    dublicates = scraper.find_duplicates(href_list)
    if dublicates:
        print(f"Дубликаты найдены: {len(dublicates)} - кол-во дубликатов")
        href_list = scraper.remove_duplicates(href_list)
    else:
        print(f"Дубликаты не нйдены")

    new_files = scraper.update_links_file_txt(f'{subcategory}.txt',href_list)
    scraper.create_and_append_csv(new_files,f'{subcategory}.csv',"women_clothes")