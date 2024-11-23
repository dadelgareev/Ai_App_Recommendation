from tensorflow.keras.applications import ResNet50
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
import numpy as np

# Загрузка модели ResNet50 без верхних слоев
base_model = ResNet50(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# Добавим слой глобального усреднения по всему изображению
model = Model(inputs=base_model.input, outputs=base_model.output)


# Функция для извлечения признаков из изображения
def extract_features(image_path, model):
    img = load_img(image_path, target_size=(224, 224))  # Загружаем и масштабируем изображение
    img_array = img_to_array(img)  # Преобразуем изображение в массив
    img_array = np.expand_dims(img_array, axis=0)  # Добавляем измерение для батча
    img_array /= 255.0  # Нормализуем пиксели в диапазон [0, 1]

    features = model.predict(img_array)  # Извлекаем признаки
    return features.flatten()  # Преобразуем многомерный массив в одномерный вектор


# Пример использования
features = extract_features('nb_530.jpg', model)


import os

# Путь к директории с изображениями
image_dir = "directory"
feature_list = []
image_list = []

# Извлечение признаков для всех изображений в директории
for img_name in os.listdir(image_dir):
    img_path = os.path.join(image_dir, img_name)
    features = extract_features(img_path, model)
    feature_list.append(features)
    image_list.append(img_name)

# Преобразуем списки в numpy массивы для удобства
feature_list = np.array(feature_list)

from scipy.spatial.distance import cosine

# Функция для поиска наиболее похожих изображений
def find_similar(image_features, feature_list, image_list, top_n=5):
    distances = [cosine(image_features, feat) for feat in feature_list]
    sorted_indices = np.argsort(distances)  # Сортируем индексы по возрастанию дистанций
    return [(image_list[i], distances[i]) for i in sorted_indices[:top_n]]

# Пример использования
query_image = 'nb_530.jpg'
query_features = extract_features(query_image, model)

# Найдем 5 наиболее похожих изображений
similar_images = find_similar(query_features, feature_list, image_list, top_n=5)
print(similar_images)

import matplotlib.pyplot as plt
from PIL import Image

# Визуализация похожих изображений
def visualize_results(similar_images):
    plt.figure(figsize=(10, 5))
    for i, (img_name, dist) in enumerate(similar_images):
        img = Image.open(os.path.join(image_dir, img_name))
        plt.subplot(1, len(similar_images), i+1)
        plt.imshow(img)
        plt.title(f"Dist: {dist:.2f}")
        plt.axis('off')
    plt.show()

# Визуализируем результаты
visualize_results(similar_images)
