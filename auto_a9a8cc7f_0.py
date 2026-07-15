"""
Module for IMAP email retrieval.

This module provides a function to connect to an IMAP server and retrieve the latest 20 unread emails.
"""

import httpx
from email import parser
import os
import getpass

class ImapClient:
    def __init__(self, host: str, user: str, password: str):
        """
        Initializes the IMAP client.

        Args:
            host (str): The hostname of the IMAP server.
            user (str): The username to use for authentication.
            password (str): The password to use for authentication.
        """
        self.host = host
        self.user = user
        self.password = password

    async def connect(self):
        """
        Connects to the IMAP server.

        Returns:
            httpx.Client: A client object for interacting with the IMAP server.
        """
        try:
            return await httpx.AsyncClient.connect(
                host=self.host,
                auth=httpx.BasicAuth(self.user, self.password),
                timeout=10
            )
        except Exception as e:
            print(f"Failed to connect to IMAP server: {e}")
            raise

    async def fetch_unread_emails(self):
        """
        Fetches the latest 20 unread emails from the IMAP server.

        Returns:
            list[bytes]: A list of bytes representing the email messages.
        """
        try:
            client = await self.connect()
            response = await client.request("SELECT", "ALL")
            headers, emails = response.content.split(b"\n\n")
            return [(parser.parse(str(email)).get_payload(decode=True).decode() for email in emails.split(",")[1:])]
        except Exception as e:
            print(f"Failed to fetch unread emails: {e}")
            raise

def main():
    host = input("Enter IMAP server hostname: ")
    user = input("Enter username: ")
    password = getpass.getpass("Enter password: ")

    client = ImapClient(host, user, password)
    emails = await client.fetch_unread_emails()

    print("\nLatest 20 unread emails:")
    for email in emails[:20]:
        print(email)

if __name__ == "__main__":
    main()