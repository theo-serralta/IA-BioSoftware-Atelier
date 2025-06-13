import os
import tempfile
import pytest
from burger_maker import (
    calculate_burger_price,
    load_last_count,
    save_burger,
    get_choice,
    get_order_timestamp
)


def test_calculate_burger_price_no_ingredients():
    assert calculate_burger_price([]) == 0.0


def test_calculate_burger_price_with_ingredients():
    # bun (2.0) + beef (5.0) * (1+0.1)^2 = 7.0 * 1.21 = 8.47 rounded
    price = calculate_burger_price(['bun', 'beef'])
    assert price == 8.47


def test_load_last_count_missing(tmp_path, monkeypatch):
    # Ensure default 0 when file missing
    monkeypatch.chdir(tmp_path)
    assert load_last_count(output_dir=str(tmp_path)) == 0


def test_save_and_load_count(tmp_path):
    # Save a burger and read back the count
    burger_data = {'id': 5, 'description': 'test'}
    output_dir = str(tmp_path)
    save_burger(burger_data, output_dir=output_dir)
    count = load_last_count(output_dir=output_dir)
    assert count == 5


def test_get_choice_valid(monkeypatch, capsys):
    monkeypatch.setattr('builtins.input', lambda prompt: 'mustard')
    choice = get_choice('Choose sauce', ('ketchup', 'mustard'), 'ketchup')
    assert choice == 'mustard'
    captured = capsys.readouterr()
    assert 'Invalid' not in captured.out


def test_get_choice_invalid(monkeypatch, capsys):
    monkeypatch.setattr('builtins.input', lambda prompt: 'invalid')
    choice = get_choice('Choose meat', ('beef', 'chicken'), 'beef')
    assert choice == 'beef'
    captured = capsys.readouterr()
    assert "defaulting to 'beef'" in captured.out.lower()


def test_get_order_timestamp_format():
    ts = get_order_timestamp()
    # ISO format should contain 'T'
    assert 'T' in ts
    # And be parseable by datetime
    from datetime import datetime
    parsed = datetime.fromisoformat(ts)
    assert isinstance(parsed, datetime)
