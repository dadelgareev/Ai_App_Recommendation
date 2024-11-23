import os
from torchvision import datasets
from torchvision import transforms
from PIL import Image

# Трансформации: конвертируем в тензор и преобразуем в формат изображений
transform = transforms.Compose([transforms.ToTensor()])

# Загрузка датасета
train_data = datasets.FashionMNIST(root='./data', train=True, download=True, transform=transform)
test_data = datasets.FashionMNIST(root='./data', train=False, download=True, transform=transform)

# Список классов (метки)
class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

# Создаем директории для каждого класса
os.makedirs("fashion_mnist_train", exist_ok=True)
os.makedirs("fashion_mnist_test", exist_ok=True)

for class_name in class_names:
    os.makedirs(f"fashion_mnist_train/{class_name}", exist_ok=True)
    os.makedirs(f"fashion_mnist_test/{class_name}", exist_ok=True)

# Сохранение тренировочных изображений
for i, (img, label) in enumerate(train_data):
    class_name = class_names[label]
    img = transforms.ToPILImage()(img)  # Преобразуем тензор обратно в изображение
    img.save(f"fashion_mnist_train/{class_name}/{i}.png")

# Сохранение тестовых изображений
for i, (img, label) in enumerate(test_data):
    class_name = class_names[label]
    img = transforms.ToPILImage()(img)
    img.save(f"fashion_mnist_test/{class_name}/{i}.png")
