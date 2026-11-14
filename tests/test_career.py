import pandas as pd
import pytest

from tennis_age.career import (
    _build_dataframe,
    _extract_match_rows,
    _normalize_player_name,
)


def test_normalize_player_name():
    assert _normalize_player_name("serena williams") == "serenawilliams"
    assert _normalize_player_name("SerenaWilliams") == "SerenaWilliams"


def test_empty_player_name():
    with pytest.raises(ValueError, match="non-empty"):
        _normalize_player_name("")


def test_parse_female_rows(female_js):
    rows = _extract_match_rows(female_js)
    data = _build_dataframe(rows, pd.Timestamp("1981-09-26"))
    assert len(data) == 3
    assert data.loc[0, "opponent"] == "Anne Miller"
    assert data.loc[2, "result"] == "won"


def test_female_age_from_birth_date(female_js):
    rows = _extract_match_rows(female_js)
    data = _build_dataframe(rows, pd.Timestamp("1981-09-26"))
    assert data.loc[0, "age_opponent"] == pytest.approx(18.78, abs=0.02)


def test_male_age_already_provided(male_js):
    rows = _extract_match_rows(male_js)
    data = _build_dataframe(rows, pd.Timestamp("1986-06-03"))
    assert data.loc[0, "age_opponent"] == pytest.approx(22.264202601)
