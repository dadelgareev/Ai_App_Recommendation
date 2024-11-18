import grpc
from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image
import torch
import image_embedding_pb2
import image_embedding_pb2_grpc
import io


class ImageEmbeddingProcessor:
    def __init__(self, model_name="google/vit-base-patch16-224"):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.processor = AutoImageProcessor.from_pretrained(model_name, use_fast=True)
        self.model = AutoModelForImageClassification.from_pretrained(model_name).to(self.device)

    def get_embedding(self, img_bytes):
        try:
            img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
            inputs = self.processor(images=img, return_tensors="pt").to(self.device)

            with torch.no_grad():
                outputs = self.model(**inputs)
            embeddings = outputs.logits
            return embeddings.squeeze().tolist()
        except Exception as e:
            print(f"Could not process image: {e}")
            return None


class ImageEmbeddingClient:
    def __init__(self, server_address="localhost:50051"):
        self.channel = grpc.insecure_channel(server_address)
        self.stub = image_embedding_pb2_grpc.ImageEmbeddingServiceStub(self.channel)

    def send_embedding(self, image_path):
        processor = ImageEmbeddingProcessor()

        # Преобразование изображения в байты
        with open(image_path, "rb") as image_file:
            img_bytes = image_file.read()

        # Генерация эмбеддинга
        embedding = processor.get_embedding(img_bytes)
        if embedding is None:
            print("Failed to get embedding.")
            return None

        # Создаем gRPC запрос с байтовыми данными изображения
        request = image_embedding_pb2.EmbeddingRequest(
            image_name=image_path,
            image_data=img_bytes
        )

        # Отправляем запрос на сервер
        response = self.stub.SendEmbedding(request)
        print("Ответ от сервера:", response.message)


if __name__ == "__main__":
    client = ImageEmbeddingClient()
    client.send_embedding("path_to_image.jpg")
