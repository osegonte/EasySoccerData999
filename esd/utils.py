"""
This module contains utility functions that are used in the project.
"""

import time
import httpx


def get_today() -> str:
    """
    Get the current date in the format "YYYY-MM-DD".

    Returns:
        str: The current date in the format "YYYY-MM-DD".
    """
    return time.strftime("%Y-%m-%d")


def get_json(url: str) -> dict:
    try:
        with httpx.Client() as client:
            response = client.get(url)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 404:
            return {}
        raise exc
