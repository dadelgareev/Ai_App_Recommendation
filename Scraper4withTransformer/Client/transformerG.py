import time
from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image
import torch

class ImageEmbeddingProcessor:
    def __init__(self, model_name="google/vit-base-patch16-224"):
        # Проверка доступности GPU
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Загрузка предобработчика и модели на GPU
        self.processor = AutoImageProcessor.from_pretrained(model_name, use_fast=True)
        self.model = AutoModelForImageClassification.from_pretrained(model_name).to(self.device)

    def get_embedding(self, image_path):
        try:
            # Загрузка и подготовка изображения
            img = Image.open(image_path).convert("RGB")
            inputs = self.processor(images=img, return_tensors="pt").to(self.device)  # Перенос на GPU

            # Извлечение эмбеддинга
            with torch.no_grad():
                outputs = self.model(**inputs)
            embeddings = outputs.logits  # Логиты как эмбеддинги
            return embeddings.squeeze()  # Убираем лишние измерения и возвращаем вектор эмбеддинга
        except Exception as e:
            print(f"Could not process image {image_path}: {e}")
            return None  # Возвращаем None, если обработка не удалась


# Пример использования класса
if __name__ == "__main__":
    image_processor = ImageEmbeddingProcessor()

    # Путь к изображению
    image_path = "image_0_MP002XW0FESC_17513305_1_v1.jpeg"

    # Измерение времени выполнения
    start_time = time.time()

    # Получение 1000-мерного эмбеддинга
    embedding = image_processor.get_embedding(image_path)
    if embedding is not None:
        print(f"Embedding vector (size {embedding.size(0)}): {embedding}")

    end_time = time.time()

    # Вывод времени и используемого устройства
    print(f"Execution time: {end_time - start_time} seconds")
    print(f"Используемое устройство: {image_processor.device}")
