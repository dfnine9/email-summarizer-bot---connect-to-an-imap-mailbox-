"""
imap_unread_fetcher.py

A self‑contained script that connects to an IMAP email server, searches for
unread messages, and prints a summary of the latest ones to standard output.

Requirements:
- Uses only the Python standard library (plus `httpx` and `anthropic` which are
  not required for the core functionality but are allowed).
- Handles connection and authentication errors with try/except blocks.
- Can be executed directly with: `python imap_unread_fetcher.py`
"""

import imaplib
import email
import os
import sys
import getpass
from typing import List, Tuple

# ----------------------------------------------------------------------
# Configuration (you can also set these via environment variables)
# ----------------------------------------------------------------------
IMAP_SERVER = os.getenv("IMAP_SERVER", "imap.example.com")
IMAP_PORT = int(os.getenv("IMAP_PORT", "993"))
IMAP_USER = os.getenv("IMAP_USER")  # required
IMAP_PASSWORD = os.getenv("IMAP_PASSWORD")  # optional – will prompt if missing
MAILBOX = os.getenv("IMAP_MAILBOX", "INBOX")
MAX_MESSAGES = int(os.getenv("IMAP_MAX_MESSAGES", "5"))  # how many newest unread msgs to show


def _login(imap: imaplib.IMAP4_SSL) -> None:
    """Perform login, prompting for a password if necessary."""
    global IMAP_PASSWORD
    if not IMAP_PASSWORD:
        IMAP_PASSWORD = getpass.getpass(prompt="IMAP password: ")
    imap.login(IMAP_USER, IMAP_PASSWORD)


def _search_unread(imap: imaplib.IMAP4_SSL) -> List[bytes]:
    """Return a list of message IDs for unread messages."""
    status, data = imap.search(None, "UNSEEN")
    if status != "OK":
        raise RuntimeError("Failed to search for unread messages.")
    # data[0] is a space‑separated bytestring of IDs
    return data[0].split()


def _fetch_message(imap: imaplib.IMAP4_SSL, msg_id: bytes) -> email.message.EmailMessage:
    """Fetch a single message by ID and return an EmailMessage object."""
    status, data = imap.fetch(msg_id, "(RFC822)")
    if status != "OK":
        raise RuntimeError(f"Failed to fetch message ID {msg_id.decode()}.")
    raw_email = data[0][1]
    return email.message_from_bytes(raw_email)


def _summarize(msg: email.message.EmailMessage) -> Tuple[str, str, str]:
    """Extract a short summary (subject, from, date) from an EmailMessage."""
    subject = msg.get("Subject", "(no subject)")
    sender = msg.get("From", "(unknown sender)")
    date = msg.get("Date", "(unknown date)")
    return subject, sender, date


def main() -> None:
    if not IMAP_USER:
        print("Error: IMAP_USER environment variable not set.", file=sys.stderr)
        sys.exit(1)

    try:
        imap = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    except Exception as exc:
        print(f"Connection error: {exc}", file=sys.stderr)
        sys.exit(1)

    try:
        _login(imap)
    except imaplib.IMAP4.error as exc:
        print(f"Authentication failed: {exc}", file=sys.stderr)
        sys.exit(1)

    try:
        imap.select(MAILBOX)
        unread_ids = _search_unread(imap)

        if not unread_ids:
            print("No unread messages found.")
            imap.logout()
            return

        # Show the newest messages first
        latest_ids = sorted(unread_ids, key=lambda x: int(x), reverse=True)[:MAX_MESSAGES]

        for msg_id in latest_ids:
            try:
                msg = _fetch_message(imap, msg_id)
                subject, sender, date = _summarize(msg)
                print("=" * 40)
                print(f"Message ID: {msg_id.decode()}")
                print(f"Date      : {date}")
                print(f"From      : {sender}")
                print(f"Subject   : {subject}")
            except Exception as e:
                print(f"Failed to process message {msg_id.decode()}: {e}", file=sys.stderr)

    except Exception as exc:
        print(f"Error during IMAP operations: {exc}", file=sys.stderr)
    finally:
        imap.logout()


if __name__ == "__main__":
    main()