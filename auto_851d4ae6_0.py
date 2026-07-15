"""
This script fetches weather data from multiple sources using API calls. 
It demonstrates how to make HTTP requests, handle errors, and print results 
to standard output. The script uses the httpx library for making the API calls 
and anthropic for handling any specific data formatting or processing needs.
"""

import httpx

def fetch_weather_data(api_url):
    try:
        response = httpx.get(api_url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()  # Return the JSON response
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e}")  # Handle HTTP errors
    except Exception as e:
        print(f"An error occurred: {e}")  # Handle other exceptions

def main():
    # List of weather API URLs (replace with actual API URLs)
    weather_apis = [
        "https://api.weatherapi.com/v1/current.json?key=YOUR_API_KEY&q=London",
        "https://api.openweathermap.org/data/2.5/weather?q=London&appid=YOUR_API_KEY"
    ]
    
    for api in weather_apis:
        weather_data = fetch_weather_data(api)
        if weather_data:
            print(weather_data)  # Print the fetched weather data

if __name__ == "__main__":
    main()