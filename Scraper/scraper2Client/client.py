import grpc
import scraper_pb2
import scraper_pb2_grpc
from scraper import LamodaScraper


class LamodaScraperClient:
    def __init__(self, address='localhost:50051'):
        self.channel = grpc.insecure_channel(address)
        self.stub = scraper_pb2_grpc.ScraperServiceStub(self.channel)

    def send_tags_by_category(self, tags_by_category):
        request = scraper_pb2.TagsByCategoryRequest(
            tags_by_category={
                category: scraper_pb2.Tags(tags=[scraper_pb2.Tag(name=tag) for tag in tags])
                for category, tags in tags_by_category.items()
            }
        )
        response = self.stub.SendTagsByCategory(request)
        print(response.status)

    def send_subcategories_by_category(self, subcategories_by_category):
        request = scraper_pb2.SubcategoriesByCategoryRequest(
            subcategories_by_category={
                category: scraper_pb2.Subcategories(subcategories=[scraper_pb2.Subcategory(name=subcat) for subcat in subcats])
                for category, subcats in subcategories_by_category.items()
            }
        )
        response = self.stub.SendSubcategoriesByCategory(request)
        print(response.status)

    def send_parsed_csv_row(self, category, csv_row):
        request = scraper_pb2.ParsedCSVRowRequest(category=category, csv_row=csv_row)
        response = self.stub.SendParsedCSVRow(request)
        print(response.status)


if __name__ == '__main__':
    client = LamodaScraperClient()
    scraper = LamodaScraper()

    # Пример отправки категорий с тегами
    tags_by_category = {
        "man_shoes": ["Осень", "Кожа", "Черный"],
        "women_shoes": ["Лето", "Текстиль", "Белый"]
    }
    client.send_tags_by_category(tags_by_category)

    # Пример отправки подкатегорий
    subcategories_by_category = {
        "man_shoes": ["Ботинки", "Кроссовки"],
        "women_shoes": ["Балетки", "Туфли"]
    }
    client.send_subcategories_by_category(subcategories_by_category)

    # Пример отправки строки из CSV
    client.send_parsed_csv_row("man_shoes", "image_path, Осень, Кожа, Черный")

    # Отправка категорий с тегами
    client.send_tags_by_category(scraper.tags)

    # Отправка подкатегорий

    scraper.populate_actual_categories()
    client.send_subcategories_by_category(scraper.actual_categories)

    # Здесь происходит формирование csv файлов для каждой подкатегории, потом считывание этих csv и отправка строк с ссылкой на картинку, айди и тегами, также отправляем строку с названием подкатегории, чтобы понимать из какого cvs файла информация
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
            for j in range(1, 2):
                scraper.get_href_list(j, href_list)
                print(f"Категория - {category_name}, {j} - страничка была загружена")

            dublicates = scraper.find_duplicates(href_list)
            if dublicates:
                print(f"Дубликаты найдены: {len(dublicates)} - кол-во дубликатов")
                href_list = scraper.remove_duplicates(href_list)
            else:
                print(f"Дубликаты не нйдены")

            scraper.save_links_to_txt(href_list,f'{subcategory}.txt')
            scraper.create_only_csv(f'{subcategory}.txt', f'{subcategory}.csv', main_category)

            info = scraper.read_tags_from_csv(f'{subcategory}.csv')
            for substring in info:
                client.send_parsed_csv_row(subcategory, substring)