from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View

from . import services

# Create your views here.


class WeatherView(View):
    def get(self, request):
        try:
            times, temps = services.fetch_weather()
            current_temp = services.get_current_temperature(temps)
            context = {
                "city": "Gdańsk",
                "current_temp": current_temp,
                "error": None,
            }
        except Exception as e:
            context = {"city": "Gdańsk", "current_temp": None, "error": str(e)}
        return render(request, "external_data/weather.html", context)


def weather_chart_view(request):
    try:
        times, temps = services.fetch_weather()
        png_bytes = services.generate_weather_chart(times, temps)
        return HttpResponse(png_bytes, content_type="image/png")
    except Exception as e:
        return HttpResponse(f"Błąd generowania wykresu: {e}", status=502)


class UsersView(View):
    def get(self, request):
        try:
            users = services.fetch_users_with_post_counts()
            total_posts = sum(u["post_count"] for u in users)
            context = {"users": users, "total_posts": total_posts, "error": None}
        except Exception as e:
            context = {"users": [], "total_posts": 0, "error": str(e)}
        return render(request, "external_data/users.html", context)


class WeatherSummaryAPIView(View):
    def get(self, request):
        try:
            summary = services.get_weather_summary()
            return JsonResponse(summary)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=502)