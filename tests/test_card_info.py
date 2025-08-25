"""Tests for card information utilities."""

import pytest
import httpx

from dealdex import get_card_info


def test_get_card_info_returns_expected_fields():
    info = get_card_info("Black Lotus")
    assert info["name"] == "Black Lotus"
    assert info["set"]
    assert info["collector_number"]


def test_get_card_info_unknown_card():
    with pytest.raises(httpx.HTTPStatusError):
        get_card_info("This Card Does Not Exist")
