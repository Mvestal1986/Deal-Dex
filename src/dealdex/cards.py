"""Utilities for fetching card information from Scryfall."""

from __future__ import annotations

from typing import Any, Dict

import httpx

SCRYFALL_NAMED_URL = "https://api.scryfall.com/cards/named"


def get_card_info(name: str) -> Dict[str, Any]:
    """Return card information from Scryfall.

    Parameters
    ----------
    name:
        The exact name of the card to look up.

    Returns
    -------
    dict
        A dictionary containing basic card details useful for searching.

    Raises
    ------
    httpx.HTTPStatusError
        If the Scryfall API returns an error status.
    """
    response = httpx.get(SCRYFALL_NAMED_URL, params={"exact": name}, timeout=10.0)
    response.raise_for_status()
    data = response.json()
    return {
        "name": data.get("name"),
        "set": data.get("set"),
        "set_name": data.get("set_name"),
        "collector_number": data.get("collector_number"),
    }
