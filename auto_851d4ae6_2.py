"""
daily_weather_report.py

This script generates a daily weather report by aggregating weather data 
from a public API. It handles errors gracefully and prints the results 
to standard output. It requires standard library modules, along with 
httpx and anthropic as dependencies.
"""

import httpx
import json

API_URL = "https://api.weatherapi.com/v1/current.json?key=YOUR_API_KEY&q=YOUR_LOCATION"

def fetch_weather_data():
    """Fetch the weather data from the API."""
    try:
        response = httpx.get(API_URL)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def generate_report(weather_data):
    """Generate a formatted weather report from the data."""
    if weather_data:
        location = weather_data['location']['name']
        temperature = weather_data['current']['temp_c']
        condition = weather_data['current']['condition']['text']
        
        report = (f"Weather Report for {location}:\n"
                  f"Temperature: {temperature}°C\n"
                  f"Condition: {condition}\n")
        print(report)
    else:
        print("No weather data available.")

if __name__ == "__main__":
    weather_data = fetch_weather_data()
    generate_report(weather_data)