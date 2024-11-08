from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from .models import WeatherCache, City, RequestHistory
from .serializers import RequestHistorySerializer, CitySerializer
from .weather_services import get_weather_data
from datetime import timedelta
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination


class MyPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class GetWeather(APIView):
    def get(self, request):
        city_name = request.query_params.get('city')
        if not city_name:
            return Response({"error": "Укажите название города."}, status=status.HTTP_400_BAD_REQUEST)

        cached_weather = WeatherCache.objects.filter(
            city__name=city_name,
            last_updated__gte=timezone.now() - timedelta(minutes=30)
        ).first()

        if cached_weather:
            return Response({
                "temperature": cached_weather.temperature,
                "pressure": cached_weather.pressure,
                "wind_speed": cached_weather.wind_speed
            })

        try:
            data = get_weather_data(city_name, request_type='web')
            RequestHistory.objects.create(
                city=City.objects.get(name=city_name),
                request_time=timezone.now(),
                request_type='web'
            )
            return Response(data)
        except ValueError as e:
            print(f"Ошибка: {str(e)}")
            RequestHistory.objects.create(
                city=City.objects.get(name=city_name),
                request_time=timezone.now(),
                request_type='web'
            )
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RequestHistoryList(generics.ListAPIView):
    queryset = RequestHistory.objects.all()
    serializer_class = RequestHistorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['request_type', 'city__name']
    ordering_fields = ['city', 'request_time']
    ordering = ['-request_time']
    pagination_class = MyPagination


class CityList(generics.ListCreateAPIView):
    queryset = City.objects.all().order_by('name')
    serializer_class = CitySerializer
    pagination_class = MyPagination


class CityDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Город успешно удален."}, status=status.HTTP_204_NO_CONTENT)
