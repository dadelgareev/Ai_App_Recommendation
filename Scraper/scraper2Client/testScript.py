from scraper import LamodaScraper

scraper = LamodaScraper()

print(scraper.tags)

scraper.populate_actual_categories()
print(scraper.actual_categories)


for main_category in scraper.list_categories:
    categories_list = scraper.get_full_width_elements(scraper.list_categories[main_category])
    for i in range(0, len(categories_list)):
        href_list = list()

        category_name = categories_list[i].get("category_name", 'Не указано')
        category_url = categories_list[i].get("category_url", 'Не указано')
        item_count = categories_list[i].get("item_count", 'Не указано')

        category_short_url = category_url.split('/')[3]
        subcategory = f'{main_category}-{category_short_url}'
        scraper.base_url = 'https://www.lamoda.ru' + category_url
        for j in range(1, int(scraper.parse_count_pages())):
            scraper.get_href_list(j, href_list)
            print(f"Категория - {category_name}, {j} - страничка была загружена")

        dublicates = scraper.find_duplicates(href_list)
        if dublicates:
            print(f"Дубликаты найдены: {len(dublicates)} - кол-во дубликатов")
            href_list = scraper.remove_duplicates(href_list)
        else:
            print(f"Дубликаты не нйдены")

        scraper.create_only_csv(f'{subcategory}.txt',f'{subcategory}.csv',main_category)

        scraper.read_tags_from_csv(f'{subcategory}.csv')
