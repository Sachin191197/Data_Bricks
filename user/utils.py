from requests import get
from django.conf import settings

from user import metadata as UserMetadata
from user import models as UserModels


def fetch_forcast(city: str, days: int):
    api_url = f'{UserMetadata.FORECAST_API_URL}?{settings.WEATHER_API_KEY}&q={city}&days={days}&aqi=no&alerts=yes'
    response = get(api_url, headers=UserMetadata.FORECAST_API_HEADER)
    return response.json()


def normalize_forecast_details(forecasts: []):
    normalize_forecast_json = []
    for forecast in forecasts:
        normalize_forecast_json.append({
            "date": forecast["date"],
            "condition": forecast["day"]["condition"]["text"],
            "icon": forecast["day"]["condition"]["icon"],
        })
    return normalize_forecast_json


def create_user_forecast_query(user_id: int, city_id: int):
    user_log = UserModels.UserQueryLog(
        user_id=user_id,
        city_id=city_id
    )
    user_log.save()
