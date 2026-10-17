
import requests
import sqlite3
import time

# 1. Подключаемся к базе данных
conn = sqlite3.connect("weather.db")
cursor = conn.cursor()

# 2. Создаём таблицу с двумя полями
cursor.execute("""
CREATE TABLE IF NOT EXISTS weather (
    date_time TEXT,
    temperature REAL
)
""")
conn.commit()
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 48.46,
    "longitude": 35.04,
    "current": "temperature_2m",
    "timezone": "Europe/Kyiv"
}
def get_weather():
    try:
        response = requests.get(
            url,
            params=params,
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        temperature = data["current"]["temperature_2m"]
        date_time = data["current"]["time"]
        cursor.execute(
            "INSERT INTO weather (date_time, temperature) VALUES (?, ?)",
            (date_time, temperature)
        )
        conn.commit()
        print("Город: Днепр")
        print("Дата и время:", date_time)
        print("Температура:", temperature, "°C")
        print("Данные сохранены в базе данных!")
        print("-" * 30)
    except requests.RequestException as error:
        print("Ошибка получения погоды:", error)
    except (KeyError, TypeError, ValueError) as error:
        print("Ошибка обработки данных:", error)
try:
    print("Сбор погоды в Днепре запущен!")
    print("Интервал: 30 минут.")
    print("Для остановки нажми Ctrl + C.")
    print("-" * 30)
    while True:
        get_weather()
        print("Следующее измерение через 30 минут...")
        time.sleep(1800)
except KeyboardInterrupt:
    print("\nСбор погоды остановлен пользователем.")
finally:
    conn.close()
    print("Соединение с базой данных закрыто.")
