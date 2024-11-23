import grpc
import lamoda_pb2
import lamoda_pb2_grpc
from scraper import LamodaScraper


class LamodaScraperClient:
    def __init__(self, channel):
        self.stub = lamoda_pb2_grpc.LamodaServiceStub(channel)

    def send_category(self, category_name):
        request = lamoda_pb2.CategoryRequest(name=category_name)
        response = self.stub.CreateCategoryDirectory(request)
        if response.success:
            print(f"Категория {category_name} была успешно создана на сервере.")
        else:
            print(f"Категория {category_name} уже существует.")

if __name__ == '__main__':
    scraper = LamodaScraper()
    with grpc.insecure_channel('localhost:50051') as channel:
        client = LamodaScraperClient(channel)

        # Пример отправки категории
        scraper.populate_actual_categories()

        for category in scraper.actual_categories:
            client.send_category(category)
