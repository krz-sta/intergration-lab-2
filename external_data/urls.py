from django.urls import path

from .views import WeatherSummaryAPIView, WeatherView, UsersView, weather_chart_view

urlpatterns = [
    path("weather/", WeatherView.as_view(), name="weather"),
    path("weather/chart.png", weather_chart_view, name="weather-chart"),
    path("users/", UsersView.as_view(), name="users-stats"),
    path("api/weather-summary/", WeatherSummaryAPIView.as_view(), name="weather-summary-api"),
]
