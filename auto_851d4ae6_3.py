"""
weather_report_emailer.py

This script automates the sending of the weather report via email. 
It fetches weather data from a public API and sends it to a specified email address.
"""

import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def fetch_weather(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

def send_email(smtp_server, smtp_port, sender_email, sender_password, recipient_email, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)

        print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")

def main():
    api_url = "https://api.openweathermap.org/data/2.5/weather?q=London&appid=YOUR_API_KEY"
    smtp_server = "smtp.example.com"
    smtp_port = 587
    sender_email = "your_email@example.com"
    sender_password = "your_password"
    recipient_email = "recipient@example.com"
    subject = "Daily Weather Report"

    weather_data = fetch_weather(api_url)
    if weather_data:
        weather_report = f"Weather in {weather_data['name']}: {weather_data['weather'][0]['description']}"
        send_email(smtp_server, smtp_port, sender_email, sender_password, recipient_email, subject, weather_report)

if __name__ == "__main__":
    main()