from celery import shared_task
from django.conf import settings
from news.models import REGIONS, Weather
import requests
from django.core.exceptions import MultipleObjectsReturned



@shared_task
def get_and_save_weather_info():
    url = "https://weatherapi-com.p.rapidapi.com/current.json"
    weather_objects = []
    for region in REGIONS:
        querystring = {"q": region[0]}
        headers = {
            "X-RapidAPI-Key": settings.RAPID_API_KEY,
            "X-RapidAPI-Host": settings.RAPID_API_HOST
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        data = response.json()

        try:
            weather = Weather.objects.get(location=querystring['q'])
            if weather.temp == data['current']['temp_c'] and weather.text == data['current']['condition']['text'] and weather.icon == data['current']['condition']['icon']:
                continue  # data has not changed, skip this region
        except Weather.DoesNotExist:
            weather = Weather(
                location=querystring['q'],
                temp=data['current']['temp_c'],
                text=data['current']['condition']['text'],
                icon=data['current']['condition']['icon'].replace('//', 'https://')
            )
        except MultipleObjectsReturned:
            # If multiple weather objects exist for this location, update the first one and delete the rest
            weathers = Weather.objects.filter(location=querystring['q'])
            weather = weathers.first()
            for extra_weather in weathers[1:]:
                extra_weather.delete()

        weather.temp = data['current']['temp_c']
        weather.text = data['current']['condition']['text']
        weather.icon = data['current']['condition']['icon'].replace('//', 'https://')
        weather.save()
        weather_objects.append(weather)

    Weather.objects.bulk_create(weather_objects, ignore_conflicts=True)



