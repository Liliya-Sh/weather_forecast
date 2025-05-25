from flask import Flask, render_template, request


from app.weather_indicators import get_weather_current_data, get_weather_hourly_data, \
    get_weather_daily_data

from app.location import location

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    """Запрос наименование города, где нужно посмотреть погоду."""
    current_data = None
    hourly_data = None
    daily_data = None
    error_message = None  # Переменная для хранения сообщения об ошибке
    city= None

    if request.method == 'POST':
        city = request.form.get('city')

        if not city or not city.strip():
            error_message = "Пожалуйста, введите название города."
        else:
            latitude, longitude = location(city)

            if latitude is not None and longitude is not None:
                current_data = get_weather_current_data(latitude, longitude)  # Получаем текущие данные о погоде
                hourly_data = get_weather_hourly_data(latitude, longitude)  # Получаем данные о погоде ежечасно
                daily_data = get_weather_daily_data(latitude, longitude)  # Получаем данные о погоде по дням
            elif latitude is None and longitude is None:
                error_message = f"Не удалось найти город: {city}. Пожалуйста, проверьте правильность ввода."
            else:
                error_message = f"Не удалось найти город: {city}. Пожалуйста, проверьте правильность ввода."

    return render_template('index.html',
                           current_data=current_data,
                           hourly_data=hourly_data,
                           daily_data=daily_data,
                           error_message=error_message,
                           city=city)  # Передаем сообщение об ошибке в шаблон
