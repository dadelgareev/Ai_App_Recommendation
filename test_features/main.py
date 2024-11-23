import numpy as np
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing import image
from sklearn.metrics.pairwise import cosine_similarity

# Функция для загрузки изображения и его предобработки
def load_and_preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(450, 450))
    img_data = image.img_to_array(img)
    img_data = np.expand_dims(img_data, axis=0)
    img_data = preprocess_input(img_data)
    return img_data

# Функция для извлечения вектора признаков
def extract_features(model, img_data):
    features = model.predict(img_data)
    return features

# Функция для вычисления косинусного сходства
def calculate_similarity(features1, features2):
    similarity = cosine_similarity(features1, features2)
    return similarity[0][0]

# Основной код
if __name__ == "__main__":
    # Загрузим предобученную модель ResNet50 (без верхних слоев)
    model = ResNet50(weights='imagenet', include_top=False, pooling='avg')

    # Пути к изображениям, которые будем сравнивать
    img_path1 = 'face1.jpg'  # Замените на путь к первому изображению
    img_path2 = 'face2.jpg'  # Замените на путь ко второму изображению

    # Загрузка и предобработка изображений
    img_data1 = load_and_preprocess_image(img_path1)
    img_data2 = load_and_preprocess_image(img_path2)

    # Извлечение векторов признаков
    features1 = extract_features(model, img_data1)
    features2 = extract_features(model, img_data2)

    # Вычисление косинусного сходства
    similarity = calculate_similarity(features1, features2)
    print(f"Cosine similarity between the two images: {similarity*100:.4f}%")

    # Интерпретация результата
    if similarity > 0.8:  # Порог можно настроить в зависимости от задачи
        print("Images are similar")
    else:
        print("Images are not similar")
