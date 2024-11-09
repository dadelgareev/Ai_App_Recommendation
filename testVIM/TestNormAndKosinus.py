from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image
import torch
import os
from torch.nn.functional import cosine_similarity
import matplotlib.pyplot as plt

# Загрузка предобработчика и модели
processor = AutoImageProcessor.from_pretrained("google/vit-base-patch16-224")
model = AutoModelForImageClassification.from_pretrained("google/vit-base-patch16-224")

# Путь к целевому изображению и директории
target_image_path = "image_0_MP002XW0J63T_21665715_1_v1.jpeg"
directory_path = "women_clothes-clothes-bluzy-rubashki/"

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

# Эмбеддинг для целевого изображения
target_embedding = get_embedding(target_image_path)
if target_embedding is None:
    raise ValueError("Target image could not be processed.")

# Списки для хранения результатов
cosine_results = []
norm_results = []

# Цикл для перебора всех изображений в директории
for filename in os.listdir(directory_path):
    if filename.lower().endswith((".jpg", ".jpeg", ".png")):  # Проверка формата файла
        image_path = os.path.join(directory_path, filename)
        current_embedding = get_embedding(image_path)  # Получаем эмбеддинг для текущего изображения

        # Пропускаем файлы, которые не удалось обработать
        if current_embedding is None:
            continue

        # Косинусное сходство
        cosine_sim = cosine_similarity(target_embedding.unsqueeze(0), current_embedding.unsqueeze(0))
        cosine_results.append((image_path, cosine_sim.item()))

        # Норма разности между векторами
        norm_difference = torch.norm(target_embedding - current_embedding, p=2).item()
        norm_results.append((image_path, norm_difference))

# Сортировка по убыванию косинусного сходства и возрастанию нормы
cosine_results = sorted(cosine_results, key=lambda x: x[1], reverse=True)
norm_results = sorted(norm_results, key=lambda x: x[1])  # Чем меньше норма, тем ближе векторы

# Визуализация для косинусного сходства
fig1, axes1 = plt.subplots(3, 5, figsize=(20, 8))
fig1.suptitle("Top 10 Most Similar Images (Cosine Similarity)")
axes1 = axes1.flatten()

# Показ целевого изображения в первом графике
target_img = Image.open(target_image_path)
axes1[0].imshow(target_img)
axes1[0].set_title("Target Image")
axes1[0].axis("off")

# Отображение топ-14 похожих изображений по косинусному сходству
for i, (image_path, similarity) in enumerate(cosine_results[:14], start=1):
    img = Image.open(image_path)
    axes1[i].imshow(img)
    axes1[i].set_title(f"Cosine: {similarity:.4f}")
    axes1[i].axis("off")

# Визуализация для нормы разности
fig2, axes2 = plt.subplots(3, 5, figsize=(20, 8))
fig2.suptitle("Top 10 Most Similar Images (Norm of Difference)")
axes2 = axes2.flatten()

# Показ целевого изображения во втором графике
axes2[0].imshow(target_img)
axes2[0].set_title("Target Image")
axes2[0].axis("off")

# Отображение топ-14 похожих изображений по норме разности
for i, (image_path, norm_val) in enumerate(norm_results[:14], start=1):
    img = Image.open(image_path)
    axes2[i].imshow(img)
    axes2[i].set_title(f"Norm: {norm_val:.4f}")
    axes2[i].axis("off")

plt.tight_layout()
plt.show()
