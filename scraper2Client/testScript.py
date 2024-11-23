from scraper import LamodaScraper

scraper = LamodaScraper()

scraper.populate_actual_categories()
print(scraper.actual_categories)

category = scraper.get_full_width_elements(scraper.list_categories["man_clothes"])

href_list = []

category_name = category[0].get("category_name", 'Не указано')
category_url = category[0].get("category_url", 'Не указано')
item_count = category[0].get("item_count", 'Не указано')

print(category_name,category_url,item_count)
category_short_url = category_url.split('/')[3]
scraper.base_url = 'https://www.lamoda.ru' + category_url

scraper.get_href_list(2, href_list)
dublicates = scraper.find_duplicates(href_list)
if dublicates:
    print(f"Дубликаты найдены: {len(dublicates)} - кол-во дубликатов")
    href_list = scraper.remove_duplicates(href_list)
else:
    print(f"Дубликаты не найдены")

#scraper.update_links_file_and_dataset(f'{"man_clothes"}-{category_short_url}.txt', f'{"man_clothes"}-{category_short_url}.csv',f'{"man_clothes"}-{category_short_url}', 2, "man_clothes")
scraper.save_links_to_txt(href_list, output_file=f'{"man_clothes"}-{category_short_url}.txt')
scraper.create_csv_and_download_images(f'{"man_clothes"}-{category_short_url}.txt',
                                       f'{"man_clothes"}-{category_short_url}.csv',
                                       f'{"man_clothes"}-{category_short_url}', "man_clothes")

