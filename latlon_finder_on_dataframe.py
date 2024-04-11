import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

# Wczytaj ramkę danych
df = pd.read_csv('mieszkanka5960.csv')  # Zastąp 'mieszkanka4500.csv' odpowiednią ścieżką do swojego pliku

# Inicjalizuj geocoder
geolocator = Nominatim(user_agent="my_geocoder")

# Iteruj przez unikalne miasta
for city in df['region'].unique():
    try:
        # Pobierz współrzędne geograficzne dla danego miasta
        location = geolocator.geocode(city)
        if location:
            latitude = location.latitude
            longitude = location.longitude

            # Skopiuj współrzędne do wszystkich wystąpień tego miasta
            df.loc[df['region'] == city, 'latitude'] = latitude
            df.loc[df['region'] == city, 'longitude'] = longitude
            
        else:
            print(f"Nie udało się znaleźć współrzędnych dla miasta: {city}")
    except GeocoderTimedOut as e:
        print(f"Błąd podczas pobierania współrzędnych dla miasta {city}: {str(e)}")

# Zapisz zmienioną ramkę danych
df.to_csv('zmodyfikowany_plik.csv', index=False)  # Zastąp 'zmodyfikowany_plik.csv' odpowiednią nazwą pliku wyjściowego
