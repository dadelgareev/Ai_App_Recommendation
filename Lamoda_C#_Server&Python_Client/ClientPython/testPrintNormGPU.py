import time
from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image
import torch
import os

# Проверка доступности GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Загрузка предобработчика и модели на GPU
processor = AutoImageProcessor.from_pretrained("google/vit-base-patch16-224", use_fast=True)
model = AutoModelForImageClassification.from_pretrained("google/vit-base-patch16-224").to(device)

# Путь к целевому изображению
target_image_path = "image_0_MP002XW0FESC_17513305_1_v1.jpeg"

# Функция для получения эмбеддинга изображения на GPU
def get_embedding(image_path):
    try:
        # Загрузка и подготовка изображения
        img = Image.open(image_path).convert("RGB")
        inputs = processor(images=img, return_tensors="pt").to(device)  # Перенос на GPU

        # Извлечение эмбеддинга
        with torch.no_grad():
            outputs = model(**inputs)
        embeddings = outputs.logits  # Логиты как эмбеддинги
        return embeddings.squeeze()  # Убираем лишние измерения
    except Exception as e:
        print(f"Could not process image {image_path}: {e}")
        return None  # Возвращаем None, если обработка не удалась

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
print(device)
