import requests
import random

# Замените <YOUR_ACCESS_KEY> на ваш ключ доступа к API Unsplash
access_key = "btTIiFulwbe6qPUHwu5t5FYuQcgMt_Cgt-a2u21fHrg"
# Параметры запроса
params = {
    "query": "cute animals",
    "orientation": "landscape",
    "count": 30,
    "client_id": access_key
}

# URL для запроса
url = "https://api.unsplash.com/photos/random"

# Отправляем запрос и получаем ответ
response = requests.get(url, params=params)

# Извлекаем список изображений из ответа
data = response.json()
# print(data[0])
# Выбираем случайное изображение и получаем его URL
random_photo = random.choice(data)
print()
photo_url = random_photo["urls"]["regular"]

# Загружаем фото и сохраняем его на диск
response = requests.get(photo_url)
with open("cute_animal.jpg", "wb") as f:
    f.write(response.content)
print()