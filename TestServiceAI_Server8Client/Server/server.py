import grpc
from concurrent import futures
import image_embedding_pb2
import image_embedding_pb2_grpc
from PIL import Image
import torch
import io
from transformers import AutoImageProcessor, AutoModelForImageClassification
import logging

class ImageEmbeddingProcessor:
    def __init__(self, model_name="google/vit-base-patch16-224"):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.processor = AutoImageProcessor.from_pretrained(model_name, use_fast=True)
        self.model = AutoModelForImageClassification.from_pretrained(model_name).to(self.device)

    def get_embedding(self, img_bytes):
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        inputs = self.processor(images=img, return_tensors="pt").to(self.device)

        with torch.no_grad():
            outputs = self.model(**inputs)
        embeddings = outputs.logits
        return embeddings.squeeze().tolist()

class ImageEmbeddingService(image_embedding_pb2_grpc.ImageEmbeddingServiceServicer):
    def __init__(self):
        self.processor = ImageEmbeddingProcessor()

    def SendEmbedding(self, request, context):
        # Извлечение эмбеддинга из данных изображения
        embedding = self.processor.get_embedding(request.image_data)
        if embedding is None:
            return image_embedding_pb2.EmbeddingResponse(
                message="Ошибка при обработке изображения."
            )

        logging.info(f"Эмбеддинг для {request.image_name} успешно получен.")
        return image_embedding_pb2.EmbeddingResponse(
            message=f"Эмбеддинг для {request.image_name} успешно получен."
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    image_embedding_pb2_grpc.add_ImageEmbeddingServiceServicer_to_server(
        ImageEmbeddingService(), server
    )
    server.add_insecure_port("[::]:50051")
    logging.info("Сервер запущен на порту 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    serve()