from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import numpy as np

# Загружаем предобученную модель ResNet50
model = ResNet50(weights='imagenet')

# Загружаем и подготавливаем изображение
img_path = 'buldog.jpg'  # Замените на путь к вашему изображению
img = image.load_img(img_path, target_size=(224, 224))
img_array = image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0)
img_array = preprocess_input(img_array)

# Предсказание класса изображения
predictions = model.predict(img_array)
decoded_predictions = decode_predictions(predictions, top=3)[0]  # Топ-3 предсказания

# Выводим результаты
for i, (imagenet_id, label, score) in enumerate(decoded_predictions):
    print(f"{i+1}: {label} ({score * 100:.2f}%)")
