import grpc
from concurrent import futures
import lamoda_pb2
import lamoda_pb2_grpc
import csv
import os


class LamodaServiceServicer(lamoda_pb2_grpc.LamodaServiceServicer):
    def __init__(self, base_categories_dir="categories"):
        self.base_categories_dir = base_categories_dir
        if not os.path.exists(self.base_categories_dir):
            os.makedirs(self.base_categories_dir)

    def CreateCategoryDirectory(self, request, context):
        category_dir = os.path.join(self.base_categories_dir, request.base_dir, request.category_name)
        os.makedirs(category_dir, exist_ok=True)

        # Создаем CSV файл для категории, если он не существует
        csv_path = os.path.join(category_dir, f"{request.category_name}.csv")
        if not os.path.exists(csv_path):
            with open(csv_path, mode='w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["image_path", "tags"])  # Заголовки CSV

        return lamoda_pb2.Response(success=True,
                                   message=f"Directory and CSV created for category: {request.category_name}")

    def AppendTagsToCategoryCSV(self, request, context):
        category_dir = os.path.join(self.base_categories_dir, request.category_name)
        csv_path = os.path.join(category_dir, f"{request.category_name}.csv")

        # Добавляем запись с тегами в CSV файл категории
        with open(csv_path, mode='a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([request.image_path, ", ".join(request.tags)])

        return lamoda_pb2.Response(success=True, message=f"Tags appended to CSV for category: {request.category_name}")

    def SaveImagesToCategory(self, request, context):
        category_dir = os.path.join(self.base_categories_dir, request.category_name)
        if not os.path.exists(category_dir):
            os.makedirs(category_dir)

        image_path = os.path.join(category_dir, request.image_name)
        with open(image_path, "wb") as image_file:
            image_file.write(request.image_data)

        return lamoda_pb2.Response(success=True,
                                   message=f"Image {request.image_name} saved in category: {request.category_name}")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    lamoda_pb2_grpc.add_LamodaServiceServicer_to_server(LamodaServiceServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Server started on port 50051.")
    server.wait_for_termination()
