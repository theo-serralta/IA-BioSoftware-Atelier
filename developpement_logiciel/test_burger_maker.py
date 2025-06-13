import os
import pytest
from datetime import datetime

# Import the module under test as a package
from . import burger


def test_calculate_burger_price_no_ingredients():
    assert burger.calculate_burger_price([]) == 0.0


def test_calculate_burger_price_with_ingredients():
    # bun (2.0) + beef (5.0) base=7.0, after two 10% taxes: 7.0 * 1.1**2 = 8.47
    price = burger.calculate_burger_price(['bun', 'beef'])
    assert price == 8.47


def test_load_last_count_missing(tmp_path, monkeypatch):
    # Ensure default 0 when count file is missing
    monkeypatch.chdir(tmp_path)
    assert burger.load_last_count(output_dir=str(tmp_path)) == 0


def test_save_and_load_count(tmp_path):
    # Save a burger and read back the count
    data = {'id': 5, 'description': 'test'}
    out = str(tmp_path)
    burger.save_burger(data, output_dir=out)
    count = burger.load_last_count(output_dir=out)
    assert count == 5


def test_get_choice_valid(monkeypatch, capsys):
    monkeypatch.setattr('builtins.input', lambda _: 'mustard')
    choice = burger.get_choice('Choose sauce', burger.SAUCE_OPTIONS, 'ketchup')
    assert choice == 'mustard'
    captured = capsys.readouterr()
    assert 'Invalid' not in captured.out


def test_get_choice_invalid(monkeypatch, capsys):
    monkeypatch.setattr('builtins.input', lambda _: 'invalid')
    choice = burger.get_choice('Choose meat', burger.MEAT_OPTIONS, 'beef')
    assert choice == 'beef'
    captured = capsys.readouterr()
    assert "defaulting to 'beef'" in captured.out.lower()


def test_get_bun_default_and_custom(monkeypatch, capsys):
    # default (empty) -> 'regular'
    monkeypatch.setattr('builtins.input', lambda _: '')
    bun = burger.get_bun()
    assert bun == 'regular'
    # custom bun
    monkeypatch.setattr('builtins.input', lambda _: 'sesame')
    bun = burger.get_bun()
    assert bun == 'sesame'


def test_get_meat_and_sauce(monkeypatch, capsys):
    # meat valid
    monkeypatch.setattr('builtins.input', lambda _: 'chicken')
    meat = burger.get_meat()
    assert meat == 'chicken'
    # sauce valid
    monkeypatch.setattr('builtins.input', lambda _: 'mustard')
    sauce = burger.get_sauce()
    assert sauce == 'mustard'


def test_get_cheese_default_and_custom(monkeypatch, capsys):
    # default
    monkeypatch.setattr('builtins.input', lambda _: '')
    cheese = burger.get_cheese()
    assert cheese == 'cheddar'
    # custom
    monkeypatch.setattr('builtins.input', lambda _: 'swiss')
    cheese = burger.get_cheese()
    assert cheese == 'swiss'


def test_get_order_timestamp_format():
    ts = burger.get_order_timestamp()
    assert 'T' in ts
    parsed = datetime.fromisoformat(ts)
    assert isinstance(parsed, datetime)


def test_assemble_burger_and_output(tmp_path, monkeypatch):
    # simulate user inputs: bun, meat, sauce, cheese
    inputs = iter(['sesame', 'beef', 'ketchup', 'gouda'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    # fix timestamp in module namespace
    monkeypatch.setattr(burger, 'get_order_timestamp', lambda: '2025-06-13T12:00:00')

    result = burger.assemble_burger(10)
    assert result['id'] == 10
    assert result['timestamp'] == '2025-06-13T12:00:00'
    assert result['description'] == 'sesame bun + beef + ketchup + gouda cheese'
    expected = burger.calculate_burger_price(['bun', 'beef', 'sauce', 'cheese'])
    assert result['price'] == expected


def test_main_creates_files(tmp_path, monkeypatch):
    # Redirect output directory to tmp and no existing count
    monkeypatch.chdir(tmp_path)
    # Override OUTPUT_DIR in module to write into tmp_path
    monkeypatch.setattr(burger, 'OUTPUT_DIR', str(tmp_path))

    # simulate inputs: bun='', meat='beef', sauce='ketchup', cheese=''
    inputs = iter(['', 'beef', 'ketchup', ''])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    # Run main
    burger.main()

    # Verify files created in tmp_path
    assert (tmp_path / 'burger.txt').exists()
    assert (tmp_path / 'burger_count.txt').read_text() == '1'
