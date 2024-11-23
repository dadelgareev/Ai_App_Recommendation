from Scrapper import LamodaScraper

url = 'https://www.lamoda.ru/c/17/shoes-men/?sitelink=topmenuM&l=4'

scrapper = LamodaScraper(url)

catalog_list = scrapper.get_catalog_href()
for type in catalog_list:
    print(f"Тип одежды: {type['type']}.Ссылка на каталог: {type['href']}")

data_set = {
    "product_id": [],
    "product_url": [],
    "product_name": [],
    "image_url": [],
    "price_new": [],
    "price_old": [],
    "matching_pics": []
}

#scrapper.scrape_page()
href_list = []
href_list = scrapper.get_href_list(1, href_list)
print(len(href_list))
href_list = scrapper.get_href_list(2, href_list)
print(len(href_list))
print(href_list)
href_list.clear()
"""
for i in range(1, int(scrapper.parse_count_pages())):
    scrapper.get_href_list(i, href_list)
    print(f"{i} - страничка была загружена")
"""
"""
scrapper.get_href_list(1, href_list)
dublicates = scrapper.find_duplicates(href_list)

if dublicates:
    print(f"Дубликаты найдены: {dublicates}")
    href_list = scrapper.remove_duplicates(href_list)
else:
    print(f"Дубликаты не нйдены")
"""

#scrapper.save_links_to_txt(href_list, output_file='1-page_men-shoes_links.txt')

url_with_item = 'https://www.lamoda.ru/p/rtlabc796406/shoes-puma-krossovki/'

result = scrapper.get_all_atrib_from_page(url_with_item)

print(result['image_urls'])  # Список URL картинок
print(result['attributes'])  # Словарь с атрибутами товара
print(result["categories"])

# Выводим только выбранные атрибуты
selected_attributes = ['Сезон','Материал подошвы','Материал верха', 'Цвет', 'Страна производства']
for key in selected_attributes:
    print(f"{key}: {result['attributes'].get(key, 'Не найдено')}")

# Преобразуем ключи словаря категорий в список
categories_keys = list(result['categories'].keys())

# Проверяем, что в словаре есть хотя бы 4 категории
if len(categories_keys) >= 5:
    fourth_category_key = categories_keys[4]  # Индексация с нуля, поэтому 3 это четвертая категория
    print(f"{fourth_category_key}: {result['categories'][fourth_category_key]}")
else:
    print("Категорий меньше 5.")

#scrapper.create_csv_from_txt('1-page_men-shoes_links.txt', 'test.cvs')
#scrapper.create_csv_and_download_images('1-page_men-shoes_links.txt', 'test.csv', 'images_1_page')
#scrapper.create_csv_and_download_images('men-shoes_links.txt', 'dataset.csv', 'images_shoes')
catalog = scrapper.get_catalog_href()
print(catalog)

scrapper2 = LamodaScraper("https://www.lamoda.ru/c/17/shoes-men/?sitelink=topmenuM&l=4")
#print(scrapper2.fetch_page())
print(scrapper2.get_full_width_elements('https://www.lamoda.ru/c/17/shoes-men/?sitelink=topmenuM&l=4'))

categories_list = scrapper2.get_full_width_elements("https://www.lamoda.ru/c/17/shoes-men/?sitelink=topmenuM&l=4")
href_list.clear()
for i in range(0, len(categories_list)):
    category_name = categories_list[i].get("category_name", 'Не указано')
    category_url = categories_list[i].get("category_url", 'Не указано')
    item_count = categories_list[i].get("item_count", 'Не указано')

    category_short_url = category_url.split('/')[3]
    scrapper2.base_url = 'https://www.lamoda.ru' + category_url
    print(category_short_url)
    print(scrapper2.base_url)
    for i in range(1, 6):
        scrapper2.get_href_list(i, href_list)
        print(f"{i} - страничка была загружена")
    dublicates = scrapper.find_duplicates(href_list)

    if dublicates:
        print(f"Дубликаты найдены: {dublicates}")
        href_list = scrapper.remove_duplicates(href_list)
    else:
        print(f"Дубликаты не нйдены")
    scrapper.save_links_to_txt(href_list, output_file=f'5-page_men-{category_short_url}.txt')
    scrapper.create_csv_and_download_images(f'5-page_men-{category_short_url}.txt', f'{category_short_url}.csv', f'{category_short_url}')
    href_list.clear()


scrapper3 = LamodaScraper("https://www.lamoda.ru/c/17/shoes-men/?sitelink=topmenuM&l=4")
"""
old_link = scrapper3.get_href_list(5)
scrapper3.save_links_to_txt(old_link, output_file=f'old-link.txt')
"""
scrapper3.update_links_file('old-link.txt')