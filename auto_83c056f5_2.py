"""
Module for creating sentiment analysis visualization using Matplotlib.

This module provides a self-contained function for creating a simple bar chart
representing sentiment analysis results.
"""

import httpx
import json
from anthropic import get_sentiment_score
import matplotlib.pyplot as plt

def visualize_sentiment_analysis():
    """
    Create a visualization of sentiment analysis results.

    This function retrieves the sentiment analysis results, sorts them by score,
    and plots them using Matplotlib's bar chart.
    """

    try:
        # Retrieve sentiment scores from Anthropic API
        response = httpx.get("https://api.anthropicevolution.com/sentiment")
        response.raise_for_status()
        data = json.loads(response.text)

        # Extract scores and labels
        scores = [result["score"] for result in data]
        labels = [result["label"] for result in data]

        # Create bar chart
        plt.bar(labels, scores)
        plt.xlabel("Sentiment Label")
        plt.ylabel("Score")
        plt.title("Sentiment Analysis Results")
        plt.show()

    except httpx.HTTPError as e:
        print(f"HTTP error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    visualize_sentiment_analysis()