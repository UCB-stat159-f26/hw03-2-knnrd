"""Retrieve and process career match data from Tennis Abstract."""

import json
import re

import pandas as pd
import requests


BASE_URL = "https://www.tennisabstract.com"
HEADERS = {"User-Agent": "Mozilla/5.0"}


def _normalize_player_name(name):
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Player name must be a non-empty string.")
    slug = re.sub(r"[^A-Za-z0-9]", "", name)
    return slug


def _download_text(url):
    response = requests.get(url, headers=HEADERS, timeout=20)
    response.raise_for_status()
    return response.text


def _extract_match_rows(js_text):
    match = re.search(r"var\s+morematchmx\s*=\s*(\[.*?\]);", js_text, re.S)
    if not match:
        raise ValueError("Career match data could not be found.")
    return json.loads(match.group(1))


def _parse_match_date(value):
    return pd.to_datetime(value, format="%Y%m%d", errors="coerce")


def _years_between(later, earlier):
    return (later - earlier).days / 365.25
