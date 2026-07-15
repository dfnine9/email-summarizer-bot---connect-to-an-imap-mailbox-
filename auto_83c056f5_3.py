"""
sentiment_analysis_report.py

This script performs sentiment analysis on a given text input and generates a report summarizing the findings.
It utilizes the httpx library to make HTTP requests and the anthropic library for sentiment analysis.
The report includes the overall sentiment and any notable points of interest.

Usage:
    python sentiment_analysis_report.py
"""

import httpx
import anthropic

def analyze_sentiment(text):
    """Analyze the sentiment of the provided text."""
    try:
        response = httpx.post("https://api.anthropic.com/v1/sentiment", json={"text": text})
        response.raise_for_status()
        sentiment_data = response.json()
        return sentiment_data['sentiment'], sentiment_data['details']
    except httpx.HTTPStatusError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

def generate_report(sentiment, details):
    """Generate a report based on the sentiment analysis findings."""
    report = f"Sentiment Analysis Report\n"
    report += f"Overall Sentiment: {sentiment}\n"
    report += "Details:\n"
    for detail in details:
        report += f"- {detail}\n"
    return report

def main():
    text = "Your input text for sentiment analysis goes here."
    sentiment, details = analyze_sentiment(text)
    
    if sentiment and details:
        report = generate_report(sentiment, details)
        print(report)

if __name__ == "__main__":
    main()