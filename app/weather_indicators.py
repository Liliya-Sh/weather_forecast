import datetime

import pandas as pd

import openmeteo_requests
import requests_cache
from retry_requests import retry


# Настройка клиента Open-Meteo API с кэшированием и повторными попытками при ошибках
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)


def get_weather_data(latitude, longitude):
    """Запрос прогноза погоды на один день"""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": ["relative_humidity_2m",
                   "apparent_temperature",
                   "precipitation_probability",
                   "cloud_cover",
                   "visibility",
                   "temperature_2m",
                   "wind_speed_10m",
                   "precipitation"],
        "current": ["temperature_2m",
                    "relative_humidity_2m",
                    "apparent_temperature",
                    "is_day",
                    "precipitation",
                    "wind_direction_10m",
                    "wind_speed_10m"],
        "forecast_days": 1,
        "temporal_resolution": "hourly_1"
    }
    responses = openmeteo.weather_api(url, params=params)
    return responses[0]


def get_weather_current_data(latitude, longitude):
    """Посмотреть текущкю погоду"""
    response = get_weather_data(latitude, longitude)
    current = response.Current()
    current_data = {
        "date": datetime.datetime.now(),
        "temperature": round(current.Variables(0).Value()),
        "humidity": current.Variables(1).Value(),
        "apparent_temperature": round(current.Variables(2).Value()),
        "is_day": current.Variables(3).Value(),
        "precipitation": current.Variables(4).Value(),
        "wind_direction": round(current.Variables(5).Value()),
        "wind_speed": round(current.Variables(6).Value())
    }

    return current_data


def get_weather_hourly_data(latitude, longitude):
    """Посмотреть погоду ежечасно"""

    response = get_weather_data(latitude, longitude)
    hourly = response.Hourly()
    hourly_data = {
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"),
        "temperature_2m": [round(temp) for temp in hourly.Variables(1).ValuesAsNumpy()],
        "precipitation": hourly.Variables(2).ValuesAsNumpy(),
    }

    return hourly_data


def get_weather_daily_data(latitude, longitude):
    """Посмотреть погоду ежедневно(7 дней)"""

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": ["temperature_2m_max",
                  "temperature_2m_min",
                  "sunrise",
                  "sunset",
                  "precipitation_probability_max",
                  "wind_speed_10m_max"]
    }
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]

    daily = response.Daily()
    daily_data = {
        "date": pd.date_range(
            start=pd.to_datetime(daily.Time(), unit="s", utc=True),
            end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=daily.Interval()),
            inclusive="left"
        ),
        "temperature_2m_max": [round(temp_max) for temp_max in daily.Variables(0).ValuesAsNumpy()],
        "temperature_2m_min": [round(temp_min) for temp_min in daily.Variables(0).ValuesAsNumpy()],
        "precipitation_probability_max": daily.Variables(2).ValuesAsNumpy(),
    }

    return daily_data
