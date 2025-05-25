from geopy import Nominatim

geolocator = Nominatim(user_agent='my_geocoder')


def location(city_name: str):
    """Ищем координаты города по наименованию."""

    loc = geolocator.geocode(city_name)

    if loc:
        latitude = loc.latitude
        longitude = loc.longitude
        print(latitude, longitude)
        return latitude, longitude

    else:
        print(f"Не удалось найти {city_name}")
        return None, None
