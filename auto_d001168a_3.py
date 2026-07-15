"""
email_triage_gmail_integration.py - Integrates Gmail API for notifications on backup completion.

This module provides a self-contained script that integrates the email triage system with Gmail API.
It uses the httpx library to send requests to the Gmail API and prints results to stdout.

Author: [Your Name]
"""

import os
import json
from httpx import Client

class EmailTriageGmailIntegration:
    def __init__(self, client_id, client_secret, refresh_token):
        """
        Initialize the Gmail API client.

        :param client_id: Google Cloud Console ID for the project.
        :param client_secret: Google Cloud Console Secret key for the project.
        :param refresh_token: Refresh token obtained from the authorization flow.
        """
        self.client = Client()
        self.client.headers.update({
            'Authorization': f'Bearer {refresh_token}',
            'Content-Type': 'application/json'
        })

    def get_user_id(self):
        """
        Get the user ID for the current authenticated user.

        :return: User ID as a string.
        """
        try:
            response = self.client.get('https://www.googleapis.com/userinfo/profile')
            return response.json()['id']
        except Exception as e:
            print(f'Error getting user ID: {e}')
            return None

    def create_notification(self, email, message):
        """
        Create a notification in the email triage system.

        :param email: Email address to send the notification to.
        :param message: Notification message.
        """
        try:
            response = self.client.post('https://example.com/api/notifications', json={
                'email': email,
                'message': message
            })
            print(response.json())
        except Exception as e:
            print(f'Error creating notification: {e}')

def main():
    client_id = os.environ['GMAIL_CLIENT_ID']
    client_secret = os.environ['GMAIL_CLIENT_SECRET']
    refresh_token = os.environ['GMAIL_REFRESH_TOKEN']

    integration = EmailTriageGmailIntegration(client_id, client_secret, refresh_token)

    user_id = integration.get_user_id()
    if user_id:
        email = 'user@example.com'  # Replace with the actual email address.
        message = 'Backup completed successfully.'
        integration.create_notification(email, message)

if __name__ == '__main__':
    main()