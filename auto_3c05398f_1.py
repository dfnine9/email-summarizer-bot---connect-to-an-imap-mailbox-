"""
Email Processor

This script fetches emails via an HTTP request, extracts key information 
such as sender, subject, and date, and summarizes the content of each email. 
It is designed to be self-contained and uses only the standard library, 
httpx, and anthropic for processing.

Usage:
    Run the script using: python script.py
"""

import httpx
import anthropic

def fetch_emails(url):
    """Fetch emails from the specified URL."""
    try:
        response = httpx.get(url)
        response.raise_for_status()
        return response.json()  # Assuming the response is in JSON format
    except httpx.HTTPStatusError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return []
    except Exception as err:
        print(f"An error occurred: {err}")
        return []

def extract_key_info(email):
    """Extract key information from an email."""
    try:
        sender = email.get('sender', 'Unknown Sender')
        subject = email.get('subject', 'No Subject')
        date = email.get('date', 'No Date')
        content = email.get('content', '')
        summary = anthropic.analyze(content)  # Hypothetical analysis method
        return {
            'sender': sender,
            'subject': subject,
            'date': date,
            'summary': summary
        }
    except Exception as err:
        print(f"Error extracting information: {err}")
        return None

def main():
    url = "http://example.com/emails"  # Replace with actual email URL
    emails = fetch_emails(url)
    
    for email in emails:
        key_info = extract_key_info(email)
        if key_info:
            print(f"Sender: {key_info['sender']}")
            print(f"Subject: {key_info['subject']}")
            print(f"Date: {key_info['date']}")
            print(f"Summary: {key_info['summary']}\n")

if __name__ == "__main__":
    main()