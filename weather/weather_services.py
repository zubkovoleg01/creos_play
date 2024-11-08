import requests
from django.utils import timezone
from datetime import timedelta
from .models import City, WeatherCache, RequestHistory


def get_coordinates(city_name):
    headers = {
        'User-Agent': 'MyWeatherApp/1.0'
    }
    response = requests.get(f"https://nominatim.openstreetmap.org/search?q={city_name}&format=json", headers=headers)

    if response.status_code != 200:
        raise ValueError(f"Ошибка при получении координат: {response.status_code} - {response.text}")

    data = response.json()
    if data:
        return float(data[0]["lat"]), float(data[0]["lon"])

    raise ValueError("Не удалось найти координаты для данного города.")


def get_weather_data(city_name, request_type):
    access_key = 'YOUR_KEY'

    try:
        coordinates = get_coordinates(city_name)
    except ValueError as e:
        raise ValueError(f"Ошибка при получении координат: {str(e)}")

    lat, lon = coordinates
    city, created = City.objects.get_or_create(name=city_name, lat=lat, lon=lon)

    cache = WeatherCache.objects.filter(city=city).first()
    if cache and timezone.now() - cache.last_updated < timedelta(minutes=30):
        return {
            "temperature": cache.temperature,
            "pressure": cache.pressure,
            "wind_speed": cache.wind_speed,
        }

    headers = {
        'X-Yandex-Weather-Key': access_key
    }
    response = requests.get(f'https://api.weather.yandex.ru/v2/forecast?lat={lat}&lon={lon}', headers=headers)

    if response.status_code == 200:
        data = response.json()
        temperature = data['fact']['temp']
        pressure = data['fact']['pressure_mm']
        wind_speed = data['fact']['wind_speed']

        WeatherCache.objects.update_or_create(
            city=city,
            defaults={
                "temperature": temperature,
                "pressure": pressure,
                "wind_speed": wind_speed,
                "last_updated": timezone.now()
            }
        )

        RequestHistory.objects.create(
            city=city,
            request_type=request_type,
            request_time=timezone.now()
        )

        return {
            "temperature": temperature,
            "pressure": pressure,
            "wind_speed": wind_speed
        }
    else:
        raise ValueError(f"Ошибка при получении данных о погоде: {response.status_code} - {response.text}")

