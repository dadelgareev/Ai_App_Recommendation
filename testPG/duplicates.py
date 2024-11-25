import pandas as pd

# Загрузка CSV файла
df = pd.read_csv('women_clothes-clothes-yubki_temp.csv')  # Замените на путь к вашему файлу

# Проверка, если колонка 'link_url' существует в файле
if 'image_url' in df.columns:
    # Считаем количество дубликатов по 'link_url'
    duplicate_counts = df['image_url'].value_counts()

    # Отфильтровываем только те значения, которые встречаются больше одного раза
    duplicates = duplicate_counts[duplicate_counts > 1]

    # Выводим количество дубликатов
    print("Количество дубликатов по 'link_url':")
    print(duplicates)
else:
    print("Колонка 'link_url' не найдена в файле.")
