import grpc
import lamoda_pb2
import lamoda_pb2_grpc
import os

class LamodaScraperClient:
    def __init__(self, server_address="localhost:50051"):
        self.channel = grpc.insecure_channel(server_address)
        self.stub = lamoda_pb2_grpc.LamodaServiceStub(self.channel)

    def create_category_directory(self, category_name, base_dir="categories"):
        request = lamoda_pb2.CategoryRequest(category_name=category_name, base_dir=base_dir)
        response = self.stub.CreateCategoryDirectory(request)
        print(response.message)

    def append_tags_to_category_csv(self, tags, image_path, category_name):
        request = lamoda_pb2.TagsRequest(tags=tags, image_path=image_path, category_name=category_name)
        response = self.stub.AppendTagsToCategoryCSV(request)
        print(response.message)

    def save_images_to_category(self, image_paths, category_name):
        for image_path in image_paths:
            with open(image_path, "rb") as image_file:
                image_data = image_file.read()
            request = lamoda_pb2.ImageRequest(image_data=image_data, image_name=os.path.basename(image_path), category_name=category_name)
            response = self.stub.SaveImagesToCategory(request)
            print(response.message)

# Пример использования
if __name__ == "__main__":
    client = LamodaScraperClient()

    # Создание директории для категории и CSV файла
    client.create_category_directory("women_shoes")

    # Добавление тегов в CSV для категории
    client.append_tags_to_category_csv(["Осень", "Кожа", "Черный"], "path/to/image1.jpg", "women_shoes")

    # Сохранение изображений в директорию категории
    image_paths = ["path/to/image1.jpg", "path/to/image2.jpg"]
    client.save_images_to_category(image_paths, "women_shoes")
