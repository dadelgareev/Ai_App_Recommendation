import grpc
import image_embedding_pb2
import image_embedding_pb2_grpc


class ImageEmbeddingClient:
    def __init__(self, server_address="localhost:50051"):
        self.channel = grpc.insecure_channel(server_address)
        self.stub = image_embedding_pb2_grpc.ImageEmbeddingServiceStub(self.channel)

    def send_image(self, image_path):
        # Читаем изображение в виде байтов
        with open(image_path, "rb") as image_file:
            img_bytes = image_file.read()

        # Формируем запрос
        request = image_embedding_pb2.EmbeddingRequest(
            image_name=image_path,
            image_data=img_bytes,
        )

        # Отправляем запрос и получаем ответ
        response = self.stub.ProcessImage(request)
        print("Эмбеддинг от сервера:", response.embedding)


if __name__ == "__main__":
    client = ImageEmbeddingClient()
    client.send_image("123.jpg")
