from rest_framework import serializers
from .models import WeatherCache, RequestHistory, City


class WeatherCacheSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherCache
        fields = '__all__'


class RequestHistorySerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(source='city.name', read_only=True)

    class Meta:
        model = RequestHistory
        fields = ['id', 'request_time', 'request_type', 'city_name']


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'

