import class_lamoda_scrap

# Использование класса
url = 'https://www.lamoda.ru/c/17/shoes-men/?sitelink=topmenuM&l=4'
scraper = class_lamoda_scrap.LamodaScraper(url)

# Скрапинг первой страницы
#scraper.scrape_page(1)

# Скрапинг второй страницы
#scraper.scrape_page(2)

#Узнать сколько страниц в категории
print(scraper.parse_count_pages())

#Получить список линков картинок с 1 первой страницы
#url_links = scraper.get_image_urls(1)
#print(url_links)

#Список картинок
url_links = []

#Здесь получаем все линки картинок со всей категории (10 страниц обрабатываем)
for i in range(1,11):
    url_links.extend(scraper.get_image_urls(i))

print(len(url_links))
#Создание директории и скачивание картинок
scraper.download_images("10_pages_men_shoes", url_links)
