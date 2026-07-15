"""
expense_categorizer.py

A self‑contained script that assigns an expense category to each transaction
using an LLM (Anthropic Claude) via the HTTPX client.

Usage:
    python expense_categorizer.py

The script defines a `categorize_transaction` function that sends the
transaction description and amount to the LLM and parses its response.
Results are printed to stdout.
"""

import os
import json
import sys
from typing import List, Dict

import httpx

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

ANTHROPIC_API_URL = "https://api.anthropic.com/v1/complete"
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

if not ANTHROPIC_API_KEY:
    sys.stderr.write("Error: ANTHROPIC_API_KEY environment variable not set.\n")
    sys.exit(1)

HEADERS = {
    "Content-Type": "application/json",
    "x-api-key": ANTHROPIC_API_KEY,
    "anthropic-version": "2023-06-01",
}

# --------------------------------------------------------------------------- #
# Core logic
# --------------------------------------------------------------------------- #

def categorize_transaction(description: str, amount: float) -> str:
    """
    Sends a request to Anthropic's Claude model to determine an expense category.

    Parameters
    ----------
    description : str
        Human‑readable description of the transaction.
    amount : float
        Transaction amount (positive for expense, negative for income).

    Returns
    -------
    str
        The category assigned by the LLM (e.g., "Travel", "Food", "Utilities").
    """
    prompt = (
        "You are an expense‑categorization assistant. "
        "Given the transaction description and amount, assign a single short "
        "category such as \"Travel\", \"Food\", \"Utilities\", \"Salary\", etc. "
        "Return only the category name without any extra text.\n\n"
        f"Description: {description}\n"
        f"Amount: {amount:.2f}\n"
        "Category:"
    )

    payload = {
        "model": "claude-2.1",
        "prompt": prompt,
        "max_tokens_to_sample": 16,
        "temperature": 0.0,
        "stop_sequences": ["\n"],
    }

    try:
        response = httpx.post(
            ANTHROPIC_API_URL,
            headers=HEADERS,
            json=payload,
            timeout=30.0,
        )
        response.raise_for_status()
        data = response.json()
        category = data.get("completion", "").strip()
        return category or "Uncategorized"
    except httpx.HTTPError as exc:
        sys.stderr.write(f"HTTP error while categorizing transaction: {exc}\n")
        return "Error"
    except json.JSONDecodeError:
        sys.stderr.write("Failed to decode JSON response from Anthropic API.\n")
        return "Error"


def main() -> None:
    """
    Example driver that processes a static list of transactions,
    categorizes each using the LLM, and prints the results.
    """
    # Example transaction data; replace with real data as needed.
    transactions: List[Dict[str, object]] = [
        {"description": "Uber ride to airport", "amount": 42.15},
        {"description": "Starbucks coffee", "amount": 4.75},
        {"description": "Monthly gym membership", "amount": 55.00},
        {"description": "Salary for July", "amount": -3000.00},
    ]

    for tx in transactions:
        description = tx["description"]
        amount = tx["amount"]
        category = categorize_transaction(description, amount)
        print(f"Description: {description}\nAmount: {amount:.2f}\nCategory: {category}\n{'-'*40}")

if __name__ == "__main__":
    main()