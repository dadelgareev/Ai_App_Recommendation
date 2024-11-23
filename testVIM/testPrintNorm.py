from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image
import torch
import os
from torch.nn.functional import cosine_similarity
import matplotlib.pyplot as plt
import time

# Загрузка предобработчика и модели
processor = AutoImageProcessor.from_pretrained("google/vit-base-patch16-224")
model = AutoModelForImageClassification.from_pretrained("google/vit-base-patch16-224")

# Путь к целевому изображению и директории
target_image_path = "image_0_MP002XW0FESC_17513305_1_v1.jpeg"
directory_path = "women_random_light/"

# Функция для получения эмбеддинга изображения
def get_embedding(image_path):
    try:
        img = Image.open(image_path).convert("RGB")  # Пробуем открыть и конвертировать изображение в RGB
        inputs = processor(images=img, return_tensors="pt")  # Предобработка
        with torch.no_grad():
            outputs = model(**inputs)  # Предсказание
        embeddings = outputs.logits  # Получаем логиты как эмбеддинги
        return embeddings.squeeze()  # Убираем лишние измерения для удобства
    except Exception as e:
        print(f"Could not process image {image_path}: {e}")
        return None  # Вернем None, если обработка не удалась

# Измерение времени выполнения
start_time = time.time()

# Эмбеддинг для целевого изображения
target_embedding = get_embedding(target_image_path)
if target_embedding is None:
    raise ValueError("Target image could not be processed.")

# Вывод нормы эмбеддинга
norm = target_embedding.norm()
end_time = time.time()

# Вывод времени и нормы
print(f"Norm of the target embedding: {norm}")
print(f"Execution time: {end_time - start_time} seconds")