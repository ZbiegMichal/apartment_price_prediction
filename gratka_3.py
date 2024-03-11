import requests
from bs4 import BeautifulSoup
import pandas as pd

def gratka(response):
    soup = BeautifulSoup(response.content, 'html.parser')

# Znajdź wszystkie znaczniki article na stronie
    articles = soup.find_all('article', class_='teaserUnified')

# Iteruj przez znalezione artykuły
    for article in articles:
        data_href = article.get('data-href', '')

        location = article.find('span', class_='teaserUnified__location').text.strip()

        title = article.find('h2', class_='teaserUnified__title').text.strip()

        params = [param.text.strip() for param in article.find('ul', class_='teaserUnified__params').find_all('li')]

        details = [detail.text.strip() for detail in article.find('ul', class_='teaserUnified__details').find_all('li')]

        price = article.find('p', class_='teaserUnified__price').text.strip()

    
    # Print the extracted information for each apartment
        print(f"Data-href: {data_href}")
        print(f"Location: {location}")
        print(f"Title: {title}")
        print(f"Params: {params}")
        print(f"Details: {details}")
        print(f"Price: {price}")
        print('=' * 50)
    data_dict = {
    'data_href': [data_href],
    'location': [location],
    'title': [title],
    'params': [params],
    'details': [details],
    'price': [price]
    }
    df = pd.DataFrame(data_dict)


for page_number in range(1, 4):  # Zakres stron do przeszukania
    url = f'https://gratka.pl/nieruchomosci/mieszkania?page={page_number}'
    response = requests.get(url)
    gratka(response)