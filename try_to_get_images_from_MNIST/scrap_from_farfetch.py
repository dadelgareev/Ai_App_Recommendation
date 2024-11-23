import requests

# URL для POST запроса
url = 'https://www.farfetch.com/de/experience-gateway'

headers_cookie = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Content-Type': 'application/json',
    'Referer': 'https://www.farfetch.com/de/shopping/women/shoes-1/items.aspx',
    'Origin': 'https://www.farfetch.com',
}

# Создаем сессию для сохранения cookies
session = requests.Session()

# Выполняем GET-запрос для получения cookies
get_response = session.get(url, headers=headers_cookie)

# Получаем cookies в формате словаря
cookies_dict = session.cookies.get_dict()

# Преобразуем cookies в строку 'cookie1=value1; cookie2=value2'
cookies_string = "; ".join([f"{key}={value}" for key, value in cookies_dict.items()])

# Заголовки запроса с добавленными cookies
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Content-Type': 'application/json',
    'Referer': 'https://www.farfetch.com/de/shopping/women/shoes-1/items.aspx',
    'Origin': 'https://www.farfetch.com',
    'Cookie': cookies_string  # Добавляем cookies в заголовок
}

# Тело POST запроса (исправленный запрос)
payload = {
    "operationName": "ProductCatalog",
    "variables": {
        "input": {
            "contextFilter": {
                "categories": ["141258", "136301"],
                "priceType": "FULL"
            },
            "filter": {},
            "negativeFilter": {},
            "sortFilter": {
                "option": "RANKING",
                "order": "ASC"
            }
        },
        "first": 96,
        "after": "OTY="
    },
    "query": """query ProductCatalog($input: ProductCatalogSearchInput!, $first: Int, $after: String) {
        productCatalog(input: $input, first: $first, after: $after) {
            ... on ProductCatalogConnection {
                edges {
                    cursor
                    node {
                        id
                        shortDescription
                        label
                        stockQuantity
                        brand {
                            name
                        }
                        images {
                            size480 {
                                url
                                alt
                            }
                            size300 {
                                url
                                alt
                            }
                        }
                    }
                }
                totalCount
                pageInfo {
                    hasPreviousPage
                    hasNextPage
                    startCursor
                    endCursor
                }
            }
        }
    }"""
}

# Отправка POST запроса с заголовками, включая cookies
response = requests.post(url, headers=headers, json=payload)

# Проверяем статус ответа и содержимое
print(f"Статус ответа: {response.status_code}")
print(f"Ответ: {response.text}")
