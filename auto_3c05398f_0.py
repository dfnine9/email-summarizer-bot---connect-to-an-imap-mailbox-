"""
This script uses the Gmail API to fetch emails from the inbox.
It handles errors and prints the fetched email subjects to stdout.
"""

import os
import json
import httpx

# Replace with your own credentials and token
CLIENT_ID = 'YOUR_CLIENT_ID'
CLIENT_SECRET = 'YOUR_CLIENT_SECRET'
REFRESH_TOKEN = 'YOUR_REFRESH_TOKEN'
TOKEN_URI = 'https://oauth2.googleapis.com/token'
GMAIL_API_URL = 'https://gmail.googleapis.com/gmail/v1/users/me/messages'

def get_access_token():
    """Fetch a new access token using the refresh token."""
    try:
        response = httpx.post(TOKEN_URI, data={
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'refresh_token': REFRESH_TOKEN,
            'grant_type': 'refresh_token'
        })
        response.raise_for_status()
        return response.json()['access_token']
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def fetch_emails(access_token):
    """Fetch emails from the user's inbox."""
    try:
        headers = {'Authorization': f'Bearer {access_token}'}
        response = httpx.get(GMAIL_API_URL, headers=headers)
        response.raise_for_status()
        return response.json().get('messages', [])
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    """Main function to execute the script."""
    access_token = get_access_token()
    if access_token:
        emails = fetch_emails(access_token)
        for email in emails:
            print(email)

if __name__ == '__main__':
    main()