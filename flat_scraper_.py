# %%
import requests
from bs4 import BeautifulSoup
import pandas as pd
import concurrent.futures



import pandas as pd

cities_df = pd.read_csv('wojewodztwa_miasta.csv',sep=',')
cities_df = cities_df[(cities_df['nazwa województwa'] == 'PODKARPACKIE') | (cities_df['nazwa województwa'] == 'MAŁOPOLSKIE') | (cities_df['nazwa województwa'] == 'LUBELSKIE')| (cities_df['nazwa województwa'] == 'ŚWIĘTOKRZYSKIE')]

# %%
from unidecode import unidecode

def remove_polish_chars(text):
    return unidecode(text)

# Zastosuj funkcję do kolumny 'nazwa miasta'
cities_df['nazwa miasta'] = cities_df['nazwa miasta'].apply(remove_polish_chars).str.lower()

cities = cities_df['nazwa miasta']

# %%
from bs4 import BeautifulSoup

def max_page_number(response):
    soup = BeautifulSoup(response.content, 'html.parser')
    pagination_links = soup.find_all('a', href=True)  # znajdź wszystkie linki z atrybutem href

    page_numbers = []
    for link in pagination_links:
        page_number = link.text.strip()  # wyciągnij tekst linku i usuń białe znaki z początku i końca
        if page_number.isdigit():  # sprawdź, czy tekst linku zawiera tylko cyfry
            page_numbers.append(int(page_number))  # dodaj numer podstrony do listy
            
    if page_numbers:
        return max(page_numbers)
    else:
        return 1

# %%
number = {}
i = 0
for city in cities:
    url = f'https://gratka.pl/nieruchomosci/mieszkania/{city}'
    response = requests.get(url, timeout=2)
    max_page = max_page_number(response)
    number[city] = max_page
    print(i,':',city,':',max_page)
    i+=1



# %%
df = pd.DataFrame(list(number.items()), columns=['miasto', 'numer_podstrony'])

# %%
df.to_csv('liczba_podstron_z_miastem.csv')
df['miasto'] = df['miasto'].str.replace(' ', '-')
df

# %%
i=0
data_href_list = []
def gratka(response):
    soup = BeautifulSoup(response.content, 'html.parser')

# Znajdź wszystkie znaczniki article na stronie
    articles = soup.find_all('article', class_='teaserUnified')
    
# Iteruj przez znalezione artykuły
    for article in articles:
        data_href = article.get('data-href', '')    
        print(i+1,data_href)  
        data_href_list.append(data_href)
        


# %%
url = f'https://gratka.pl/nieruchomosci/mieszkania/ciechocinek?page=1'
response = requests.get(url, timeout=10)
print(gratka(response))

# %%
for i in range(len(df)):     
  for liczba in range(df['numer_podstrony'][i]):
      # Zakres stron do przeszukania
    url = f'https://gratka.pl/nieruchomosci/mieszkania/{df['miasto'][i]}?page={liczba}'
    response = requests.get(url, timeout=10)
    print(gratka(response))

# %%
pd.DataFrame(data_href_list).to_csv('linki1.csv')

# %%
len(data_href_list)

# %%
linki = pd.read_csv('linki1.csv')

# %%
linki

# %%
from multiprocessing.pool import ThreadPool
import pandas as pd
from bs4 import BeautifulSoup

def gratka1(response):
    soup = BeautifulSoup(response.content, 'html.parser')

    data_dict = {}

    try:
        data_dict['region'] = soup.select_one('.offerLocation__region').text.strip()
    except AttributeError:
        data_dict['region'] = ''

    try:
        data_dict['title'] = soup.select_one('.sticker__title').text.strip()
    except AttributeError:
        data_dict['title'] = ''

    try:
        data_dict['total_price'] = soup.select_one('.priceInfo__value').text.strip()
    except AttributeError:
        data_dict['total_price'] = ''

    try:
        data_dict['additional_price_per_m2'] = soup.select_one('.priceInfo__additional').text.strip()
    except AttributeError:
        data_dict['additional_price_per_m2'] = ''

    try:
        opis = soup.find('div', class_='description__rolled ql-container').text.strip()
    except AttributeError:
        opis = ''
    data_dict['opis'] = opis

    li_elements = soup.select('.parameters__singleParameters li')
    for li in li_elements:
        span = li.find('span')
        value = li.find('b', class_='parameters__value')

        if span and value:
            span_text = span.text.strip()
            value_text = value.text.strip()
            data_dict[span_text] = value_text

    li_elements1 = soup.select('.parameters__groupedParameters li')
    for li1 in li_elements1:
        liw = li1.get('data-cy')
        lit = li1.text.strip()
        data_dict[liw] = lit

    img_elements = soup.select('div.gallery__container img')
    src_values = [img['src'] for img in img_elements]
    combined_src = ' '.join(src_values)
    data_dict['links_pictures'] = combined_src

    return pd.DataFrame(data_dict, index=[0])

def process_responses(responses):
    with ThreadPool() as pool:
        results = pool.map(gratka1, responses)

    return pd.concat(results, ignore_index=True)




# %%
import pandas as pd
import requests

df1 = pd.DataFrame()

i = 0
for idx in range(0, len(linki['0'])):  
    url = linki['0'][idx]
    print(i)
    i += 1
    response = requests.get(url)
    if response.status_code == 200:
        a = gratka1(response)  # Zakładam, że ta funkcja zwraca DataFrame
        
        # Dodaj kolumnę z URL do DataFrame a
        a['URL'] = url  # Dodaje kolumnę 'URL' z aktualnym URL
        
        # Połącz wynik z ramką danych w każdej iteracji
        df1 = pd.concat([df1, a], ignore_index=True)
    else:
        print(f"Nieudane żądanie dla URL: {url}")

# Wyświetl zaktualizowaną ramkę danych
print(df1)

# %%
df1

# %%
df1.to_csv('mieszkanka1648.csv')

# %%
# Dzielimy każdy adres po słowie "ul."
df1['Część_po_ul'] = df1['title'].str.split('ul.').str.get(1).str.strip()

# Wyświetlamy ramkę danych z nową kolumną
df1['Część_po_ul']

# %%
df1['Lokalizacja']


