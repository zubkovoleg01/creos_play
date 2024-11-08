from django.urls import path
from .views import GetWeather, RequestHistoryList, CityList, CityDetail

urlpatterns = [
    path('weather/', GetWeather.as_view(), name='get-weather'),
    path('requests/', RequestHistoryList.as_view(), name='request-history'),
    path('cities/', CityList.as_view(), name='city-list'),
    path('cities/<int:pk>/', CityDetail.as_view(), name='city-detail'),
]