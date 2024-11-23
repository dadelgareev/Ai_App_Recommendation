import os
from concurrent import futures
import grpc
import lamoda_pb2
import lamoda_pb2_grpc

class LamodaServiceServicer(lamoda_pb2_grpc.LamodaServiceServicer):
    def CreateCategoryDirectory(self, request, context):
        category_name = request.name
        directory_path = f"./{category_name}"

        # Создаём директорию, если она не существует
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            # Создаём CSV файл с именем категории, если его нет
            csv_path = os.path.join(directory_path, f"{category_name}.csv")
            if not os.path.exists(csv_path):
                with open(csv_path, 'w') as csv_file:
                    csv_file.write("image_path,Категория,Сезон,Цвет,Узор,Фасон\n")
            return lamoda_pb2.CategoryResponse(success=True)
        else:
            # Директория уже существует
            return lamoda_pb2.CategoryResponse(success=False)

    def upload_images(self, image_paths):
        for image_path in image_paths:
            with open(image_path, "rb") as image_file:
                image_data = image_file.read()
            request = lamoda_pb2.ImageRequest(image_data=image_data, image_name=os.path.basename(image_path))
            response = self.stub.SaveImages(request)
            print(response.message)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    lamoda_pb2_grpc.add_LamodaServiceServicer_to_server(LamodaServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC server is running on port 50051...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
