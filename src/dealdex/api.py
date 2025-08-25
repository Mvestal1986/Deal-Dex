"""FastAPI application exposing card information endpoints."""

from __future__ import annotations

import httpx
from fastapi import FastAPI, HTTPException

from .cards import get_card_info

app = FastAPI(title="Deal-Dex API")


@app.get("/cards/{name}")
def read_card(name: str) -> dict[str, str | None]:
    """Fetch card information by name.

    Parameters
    ----------
    name:
        Exact card name to look up.

    Returns
    -------
    dict
        Basic card details from Scryfall.
    """
    try:
        return get_card_info(name)
    except httpx.HTTPStatusError as exc:  # pragma: no cover - network failure paths
        raise HTTPException(
            status_code=exc.response.status_code, detail="Card not found"
        )
