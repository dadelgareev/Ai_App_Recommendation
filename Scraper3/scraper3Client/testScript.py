from scraper import LamodaScraper

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

scraper.get_href_list(3, href_list)

new_links = scraper.update_links_file_txt(f'{subcategory}.txt', href_list)
new_tags = scraper.append_to_existing_csv(new_links, f'{subcategory}.csv', "man_shoes")
print(new_tags)