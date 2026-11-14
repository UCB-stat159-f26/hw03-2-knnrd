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


def _opponent_age(row, match_date):
    value = str(row[16]).strip()
    if re.fullmatch(r"\d{8}", value):
        birth_date = pd.to_datetime(value, format="%Y%m%d")
        return _years_between(match_date, birth_date)
    try:
        return float(value)
    except ValueError:
        return float("nan")


def _result_label(value):
    return "won" if str(value).upper() == "W" else "lost"


def _row_to_record(row, player_birth_date):
    match_date = _parse_match_date(row[0])
    player_age = _years_between(match_date, player_birth_date)
    opponent_age = _opponent_age(row, match_date)
    return {
        "date_match": match_date,
        "tournament": row[1],
        "surface": row[2],
        "age_player": player_age,
        "age_opponent": opponent_age,
        "age_diff": player_age - opponent_age,
        "opponent": row[11],
        "result": _result_label(row[4]),
    }


def _build_dataframe(rows, player_birth_date):
    records = [_row_to_record(row, player_birth_date) for row in rows]
    data = pd.DataFrame(records)
    return data.dropna(subset=["date_match", "age_player", "age_opponent"])


def _slug_candidates(player_name):
    compact = _normalize_player_name(player_name)
    words = re.findall(r"[A-Za-z0-9]+", player_name)
    title_slug = "".join(word.capitalize() for word in words)
    return list(dict.fromkeys([compact, title_slug]))


def _fetch_career_js(player_name):
    for slug in _slug_candidates(player_name):
        url = f"{BASE_URL}/jsmatches/{slug}Career.js"
        try:
            return slug, _download_text(url)
        except requests.RequestException:
            continue
    raise ValueError(f"No Tennis Abstract career data found for '{player_name}'.")


def get_career_matches(player_name):
    """Return cleaned career match data for a Tennis Abstract player."""
    slug, js_text = _fetch_career_js(player_name)
    try:
        rows = _extract_match_rows(js_text)
    except ValueError as exc:
        raise ValueError(
            f"No Tennis Abstract career data found for '{player_name}'."
        ) from exc
    birth_date = _birth_date_from_player_pages(slug)
    return _build_dataframe(rows, birth_date)


def _parse_birth_date_text(text):
    patterns = [
        r"\((\d{2}-[A-Za-z]{3}-\d{4})\)",
        r"(\d{4}-\d{2}-\d{2})",
        r"(\d{8})",
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return pd.to_datetime(match.group(1), errors="coerce")
    return None


def _birth_date_from_player_pages(slug):
    paths = ["player-classic.cgi", "wplayer-classic.cgi"]
    for path in paths:
        url = f"{BASE_URL}/cgi-bin/{path}?p={slug}"
        birth_date = _parse_birth_date_text(_download_text(url))
        if birth_date is not None and not pd.isna(birth_date):
            return birth_date
    raise ValueError("Player date of birth could not be determined.")
