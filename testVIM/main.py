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
target_image_path = "image_0_MP002XM0AY88_20478963_1_v1.jpeg"
directory_path = "man_clothes-clothes-muzhskie-bryuki/"

# Функция для получения эмбеддинга изображения
def get_embedding(image_path):
    img = Image.open(image_path)  # Загрузка изображения
    inputs = processor(images=img, return_tensors="pt")  # Предобработка
    with torch.no_grad():
        outputs = model(**inputs)  # Предсказание
    embeddings = outputs.logits  # Получаем логиты как эмбеддинги
    return embeddings.squeeze()  # Убираем лишние измерения для удобства

# Эмбеддинг для целевого изображения (Эмбеддинг - оказывается синоним к слову векторное представление)
target_embedding = get_embedding(target_image_path)

# Список для хранения результатов: каждый элемент - (путь к изображению, схожесть)
results = []

# Цикл для перебора всех изображений в директории
for filename in os.listdir(directory_path):
    if filename.endswith(".jpg") or filename.endswith(".png"):  # Проверка формата файла
        image_path = os.path.join(directory_path, filename)

        # Получаем эмбеддинг для текущего изображения
        current_embedding = get_embedding(image_path)

        # Вычисляем косинусное сходство между целевым и текущим изображением
        similarity = cosine_similarity(target_embedding.unsqueeze(0), current_embedding.unsqueeze(0))

        # Добавляем результат в список
        results.append((image_path, similarity.item()))

# Сортировка по убыванию сходства
results = sorted(results, key=lambda x: x[1], reverse=True)

# Отображаем целевое изображение и топ-10 похожих изображений
print("Top 10 most similar images:")
fig, axes = plt.subplots(3, 5, figsize=(20, 8))  # Создаем сетку 2x5 для отображения изображений
axes = axes.flatten()

# Показ целевого изображения в первом графике
target_img = Image.open(target_image_path)
axes[0].imshow(target_img)
axes[0].set_title("Target Image")
axes[0].axis("off")

# Отображение топ-14 похожих изображений
for i, (image_path, similarity) in enumerate(results[:14], start=1):
    img = Image.open(image_path)
    axes[i].imshow(img)
    axes[i].set_title(f"Similarity: {similarity:.4f}")
    axes[i].axis("off")

plt.tight_layout()
plt.show()
