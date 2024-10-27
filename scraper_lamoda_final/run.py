from scraper import LamodaScraper

scraper = LamodaScraper()

for main_category in scraper.list_categories:
    categories_list = scraper.get_full_width_elements(scraper.list_categories[main_category])
    for i in range(0, len(categories_list)):
        href_list = list()
        
        category_name = categories_list[i].get("category_name", 'Не указано')
        category_url = categories_list[i].get("category_url", 'Не указано')
        item_count = categories_list[i].get("item_count", 'Не указано')

        category_short_url = category_url.split('/')[3]
        scraper.base_url = 'https://www.lamoda.ru' + category_url
        for j in range(1, scraper.parse_count_pages()):
            scraper.get_href_list(j, href_list)
            print(f"Категория - {category_name}, {j} - страничка была загружена")

        dublicates = scraper.find_duplicates(href_list)
        if dublicates:
            print(f"Дубликаты найдены: {len(dublicates)} - кол-во дубликатов")
            href_list = scraper.remove_duplicates(href_list)
        else:
            print(f"Дубликаты не нйдены")
        scraper.save_links_to_txt(href_list, output_file=f'{main_category}-{category_short_url}.txt')
        scraper.create_csv_and_download_images(f'{main_category}-{category_short_url}.txt', f'{main_category}-{category_short_url}.csv',f'{main_category}-{category_short_url}', main_category)
        href_list.clear()

"""
categories_list = scraper.get_full_width_elements(scraper.list_categories["women_clothes"])
for i in range(0, len(categories_list)):
    href_list = list()

    category_name = categories_list[i].get("category_name", 'Не указано')
    category_url = categories_list[i].get("category_url", 'Не указано')
    item_count = categories_list[i].get("item_count", 'Не указано')

    category_short_url = category_url.split('/')[3]
    scraper.base_url = 'https://www.lamoda.ru' + category_url
    for j in range(1, 3):
        scraper.get_href_list(j, href_list)
        print(f"Категория - {category_name}, {j} - страничка была загружена")

    dublicates = scraper.find_duplicates(href_list)
    if dublicates:
        print(f"Дубликаты найдены: {len(dublicates)} - кол-во дубликатов")
        href_list = scraper.remove_duplicates(href_list)
    else:
        print(f"Дубликаты не нйдены")
    scraper.save_links_to_txt(href_list, output_file=f'{"women_clothes"}-{category_short_url}.txt')
    scraper.create_csv_and_download_images(f'{"women_clothes"}-{category_short_url}.txt',
                                           f'{"women_clothes"}-{category_short_url}.csv',
                                           f'{"women_clothes"}-{category_short_url}', "women_clothes")
    href_list.clear()



"""