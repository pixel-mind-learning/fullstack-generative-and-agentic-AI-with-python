import os
from google import genai
from dotenv import load_dotenv
import requests

load_dotenv()

# Configure Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def get_weather(city: str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t+%w+%h"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is: {response.text}"

    return f"Could not retrieve weather information for {city}. Please try again."


def main():
    user_query = input("> ")

    # Choose a model: "gemini-3.6-flash" (fast) or "gemini-1.5-pro" (more powerful)
    response = client.models.generate_content(
        model="gemini-3.6-flash", contents=user_query
    )

    print(f": {response.text}")


if __name__ == "__main__":
    # main()
    print(get_weather("Gampaha"))