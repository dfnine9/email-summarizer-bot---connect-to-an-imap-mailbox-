"""
This script fetches weather data from a public API, parses the JSON response,
aggregates the relevant information, and prints it in a structured format.

Dependencies:
- httpx (for making HTTP requests)
- anthropic (for any required functionality)

Usage:
Run the script with the command: python script.py
"""

import httpx
import json

def fetch_weather_data(api_url):
    """Fetch weather data from the provided API URL."""
    try:
        response = httpx.get(api_url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
    except httpx.RequestError as e:
        print(f"An error occurred while requesting data: {e}")
        return None
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e}")
        return None

def aggregate_weather_data(data):
    """Aggregate relevant weather data from the JSON response."""
    if not data:
        return "No data available."

    try:
        # Example aggregation (customize as needed)
        temperature = data['main']['temp']
        weather_description = data['weather'][0]['description']
        city = data['name']

        aggregated_data = {
            'City': city,
            'Temperature (°C)': temperature,
            'Weather Description': weather_description
        }
        return aggregated_data
    except KeyError as e:
        print(f"Key error: {e}")
        return "Error aggregating data."

def main():
    api_url = "https://api.openweathermap.org/data/2.5/weather?q=London&appid=YOUR_API_KEY&units=metric"
    weather_data = fetch_weather_data(api_url)
    aggregated_data = aggregate_weather_data(weather_data)
    
    print(json.dumps(aggregated_data, indent=4))

if __name__ == "__main__":
    main()