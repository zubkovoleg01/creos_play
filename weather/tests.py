from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import City, RequestHistory, WeatherCache
from django.utils import timezone
from datetime import timedelta


class WeatherAPITests(APITestCase):
    def setUp(self):
        # Создание тестовых данных
        self.city = City.objects.create(name='Test City', lat=0.0, lon=0.0)
        self.weather_cache = WeatherCache.objects.create(
            city=self.city,
            temperature=25,
            pressure=100,
            wind_speed=1,
            last_updated=timezone.now() - timedelta(minutes=5)
        )
        self.history = RequestHistory.objects.create(
            city=self.city,
            request_time=timezone.now(),
            request_type='web'
        )

    def test_get_weather(self):
        """Тест получения погоды для города"""
        url = reverse('get-weather')
        response = self.client.get(url, {'city': self.city.name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['temperature'], self.weather_cache.temperature)
        self.assertEqual(response.data['pressure'], self.weather_cache.pressure)
        self.assertEqual(response.data['wind_speed'], self.weather_cache.wind_speed)

    def test_request_history_list(self):
        """Тест получения истории запросов"""
        url = reverse('request-history')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_city_list(self):
        """Тест получения списка городов"""
        url = reverse('city-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_city_detail(self):
        """Тест получения деталей о городе"""
        url = reverse('city-detail', args=[self.city.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.city.name)

    def test_create_city(self):
        """Тест создания нового города"""
        url = reverse('city-list')
        data = {'name': 'New City', 'lat': 1.0, 'lon': 1.0}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New City')

    def test_update_city(self):
        """Тест обновления информации о городе"""
        url = reverse('city-detail', args=[self.city.id])
        data = {'name': 'Updated City', 'lat': 2.0, 'lon': 2.0}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated City')

    def test_delete_city(self):
        """Тест удаления города"""
        url = reverse('city-detail', args=[self.city.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
