def get_weather(city: str) -> str:

    weather_data = {
        "gampaha": "28°C, partly cloudy",
        "colombo": "30°C, sunny",
        "kandy": "24°C, cloudy",
        "delhi": "32°C, sunny",
    }

    return weather_data.get(
        city.lower(), f"Weather information for {city} is unavailable."
    )
