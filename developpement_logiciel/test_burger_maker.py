"""Unit tests for burger.py."""

from datetime import datetime
from developpement_logiciel import burger

def test_calculate_burger_price_no_ingredients() -> None:
    """Calculating price with no ingredients returns 0.0."""
    assert burger.calculate_burger_price([]) == 0.0


def test_calculate_burger_price_with_ingredients() -> None:
    """Calculating price with bun and beef yields correct taxed price."""
    price = burger.calculate_burger_price(["bun", "beef"])
    assert price == 8.47


def test_load_last_count_missing(tmp_path) -> None:
    """Missing count file yields default count of 0."""
    assert burger.load_last_count(output_dir=str(tmp_path)) == 0


def test_save_and_load_count(tmp_path) -> None:
    """Saving and loading count through files works correctly."""
    data = {"id": 5, "description": "test"}
    burger.save_burger(data, output_dir=str(tmp_path))
    assert burger.load_last_count(output_dir=str(tmp_path)) == 5


def test_get_choice_valid(monkeypatch, capsys) -> None:
    """Valid choice returns user selection without error message."""
    monkeypatch.setattr("builtins.input", lambda _: "mustard")
    choice = burger.get_choice("Choose sauce", burger.SAUCE_OPTIONS, "ketchup")
    captured = capsys.readouterr()
    assert choice == "mustard"
    assert not captured.out


def test_get_choice_invalid(monkeypatch, capsys) -> None:
    """Invalid choice prints defaulting message and returns default."""
    monkeypatch.setattr("builtins.input", lambda _: "invalid")
    choice = burger.get_choice("Choose meat", burger.MEAT_OPTIONS, "beef")
    captured = capsys.readouterr()
    assert choice == "beef"
    assert "defaulting to 'beef'" in captured.out.lower()


def test_get_bun_default_and_custom(monkeypatch, capsys) -> None:
    """Empty input defaults to 'regular', custom input is returned."""
    monkeypatch.setattr("builtins.input", lambda _: "")
    assert burger.get_bun() == "regular"
    monkeypatch.setattr("builtins.input", lambda _: "sesame")
    assert burger.get_bun() == "sesame"


def test_get_meat_and_sauce(monkeypatch) -> None:
    """get_meat and get_sauce return valid options."""
    monkeypatch.setattr("builtins.input", lambda _: "chicken")
    assert burger.get_meat() == "chicken"
    monkeypatch.setattr("builtins.input", lambda _: "mustard")
    assert burger.get_sauce() == "mustard"


def test_get_cheese_default_and_custom(monkeypatch) -> None:
    """Empty input defaults to 'cheddar', custom input is returned."""
    monkeypatch.setattr("builtins.input", lambda _: "")
    assert burger.get_cheese() == "cheddar"
    monkeypatch.setattr("builtins.input", lambda _: "swiss")
    assert burger.get_cheese() == "swiss"


def test_get_order_timestamp_format() -> None:
    """Timestamp returned is ISO formatted."""
    ts = burger.get_order_timestamp()
    assert "T" in ts
    datetime.fromisoformat(ts)


def test_assemble_burger_and_output(monkeypatch) -> None:
    """assemble_burger returns correct data structure and values."""
    inputs = iter(["sesame", "beef", "ketchup", "gouda"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    monkeypatch.setattr(burger, "get_order_timestamp", lambda: "2025-06-13T12:00:00")
    result = burger.assemble_burger(10)
    assert result["id"] == 10
    assert result["timestamp"] == "2025-06-13T12:00:00"
    assert result["description"] == "sesame bun + beef + ketchup + gouda cheese"
    assert result["price"] == burger.calculate_burger_price([
        "bun", "beef", "sauce", "cheese"
    ])


def test_main_creates_files(tmp_path, monkeypatch) -> None:
    """main() writes burger and count files to OUTPUT_DIR."""
    monkeypatch.setattr(burger, "OUTPUT_DIR", str(tmp_path))
    inputs = iter(["", "beef", "ketchup", ""])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    burger.main()
    assert (tmp_path / "burger.txt").exists()
    assert (tmp_path / "burger_count.txt").read_text() == "1"
