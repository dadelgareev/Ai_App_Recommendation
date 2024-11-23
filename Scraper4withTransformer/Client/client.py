import grpc
import scraper_pb2
import scraper_pb2_grpc
from scraper import LamodaScraper


class LamodaScraperClient:
    def __init__(self, host='localhost', port=50051):
        self.channel = grpc.insecure_channel(f"{host}:{port}")
        self.stub = scraper_pb2_grpc.ScraperServiceStub(self.channel)

    # Клиент для метода 1
    def send_category_info(self, category, subcategory, tags):
        request = scraper_pb2.CategoryInfoRequest(category=category, subcategory=subcategory, tags=tags)
        response = self.stub.SendCategoryInfo(request)
        print(f"Ответ сервера: {response.message}")

    # Клиент для метода 2
    def send_csv_info(self, subcategory, tags):
        request = scraper_pb2.SubcategoryInfoRequest(subcategory=subcategory, tags=tags)
        response = self.stub.SendSubcategoryInfo(request)
        print(f"Ответ сервера: {response.message}")

    # Клиент для метода 3
    def update_csv_info(self, subcategory, new_tags):
        request = scraper_pb2.UpdateSubcategoryTagsRequest(subcategory=subcategory, tags=new_tags)
        response = self.stub.UpdateSubcategoryTags(request)
        print(f"Ответ сервера: {response.message}")


if __name__ == '__main__':
    client = LamodaScraperClient()
    scraper = LamodaScraper()

    # Пример отправки категорию, подкатегории и список тегов, которые должны быть у категории:
    client.send_category_info("man_shoes", "man_shoes-krossovki", "Цвет")

    # Пример отправки подкатегории и строчки из cvs:
    client.send_csv_info("man_shoes-krossovki", "https:псевдо-ссылка.com, id, Кроссовки, Зима, резина, текстиль, черный")

    # фактически тоже, самое но благодаря нзванию сервиса, сервер должен понимать, что у нас такая (таблица, дальше уже как придумаем) - существует и надо бы дополнить ее.
    client.update_csv_info("man_shoes-krossovki", "https:псевдо-ссылка.com, id, Кроссовки, Зима, резина, текстиль, черный")

    scraper.populate_actual_categories()
    scraper.combine_category_data()

    for data in scraper.combined_data:
        client.send_category_info(data[0],data[1],data[2])

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
        print(f"Дубликаты не найдены")

    scraper.save_links_to_txt(href_list, f'{subcategory}.txt')
    scraper.create_only_csv(f'{subcategory}.txt',f'{subcategory}.csv',"man_shoes")

    info = scraper.read_tags_from_csv(f'{subcategory}.csv')
    for substring in info:
        client.send_csv_info(subcategory, substring)

"""
    # Здесь происходит формирование csv файлов для каждой подкатегории, потом считывание этих csv и отправка строк с ссылкой на картинку, айди и тегами, также отправляем строку с названием подкатегории, чтобы понимать из какого cvs файла информация
    for main_category in scraper.list_categories:
        categories_list = scraper.get_full_width_elements(scraper.list_categories[main_category])
        for i in range(0, len(categories_list)):
            href_list = list()

            category_name = categories_list[i].get("category_name", 'Не указано')
            category_url = categories_list[i].get("category_url", 'Не указано')
            item_count = categories_list[i].get("item_count", 'Не указано')

            category_short_url = category_url.split('/')[3]
            subcategory = f'{"man_shoes"}-{category_short_url}'
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

            scraper.save_links_to_txt(href_list, f'{subcategory}.txt')
            scraper.create_only_csv(f'{subcategory}.txt',f'{subcategory}.csv',main_category)

            info = scraper.read_tags_from_csv(f'{subcategory}.csv')
            for substring in info:
                client.send_csv_info(subcategory, substring)

    # повторно проходимся по всем позициям каждой категории и записываем новые позиции
    for main_category in scraper.list_categories:
        categories_list = scraper.get_full_width_elements(scraper.list_categories[main_category])
        for i in range(0, len(categories_list)):
            href_list = list()

            category_name = categories_list[i].get("category_name", 'Не указано')
            category_url = categories_list[i].get("category_url", 'Не указано')
            item_count = categories_list[i].get("item_count", 'Не указано')

            category_short_url = category_url.split('/')[3]
            subcategory = f'{"man_shoes"}-{category_short_url}'
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

            new_links = scraper.update_links_file_txt(f'{subcategory}.txt', href_list)
            new_tags = scraper.append_to_existing_csv(new_links, f'{subcategory}.csv', main_category)

            for substring in new_tags:
                client.update_csv_info(subcategory, substring)

"""





