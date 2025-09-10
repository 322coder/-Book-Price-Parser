import requests
from bs4 import BeautifulSoup
import pandas as pd

# Настройки
URL = "https://www.labirint.ru/genres/2308/"  # Страница с новинками
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

try:
    # 1. Получение страницы
    response = requests.get(URL, headers=HEADERS)
    response.raise_for_status()  # Проверка на ошибки HTTP
    
    # 2. Парсинг HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    books = soup.find_all('div', class_='product need-watch')  # Карточки книг

    # 3. Извлечение данных
    titles = []
    prices = []
    for book in books:
        # Извлечение названия
        title_elem = book.find('span', class_='product-title')
        title = title_elem.get_text(strip=True) if title_elem else 'Нет названия'
        titles.append(title)
        
        # Извлечение цены
        price_elem = book.find('span', class_='price-val')
        if price_elem:
            price = price_elem.get_text(strip=True).replace(' ', '')
        else:
            price = 'Нет цены'
        prices.append(price)

    # 4. Сохранение в Excel
    df = pd.DataFrame({
        'Название': titles,
        'Цена, руб': prices
    })
    
    df.to_excel('labirint_books.xlsx', index=False)
    print("✅ Данные сохранены в файл labirint_books.xlsx")
    print(f"📊 Обработано книг: {len(df)}")

except Exception as e:
    print(f"❌ Ошибка: {e}")