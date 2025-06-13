import logging
from datetime import datetime

from developpement_logiciel.burger import (
    assemble_burger,
    calculate_burger_price,
    get_bun,
    get_cheese,
    get_choice,
    get_meat,
    get_order_timestamp,
    get_sauce,
    load_last_count,
    main,
    save_burger,
)


def test_calculate_burger_price_no_ingredients() -> None:
    """Empty ingredients list yields zero price."""
    assert calculate_burger_price([]) == 0.0   # nosec B101

def test_calculate_burger_price_with_ingredients() -> None:
    """Correctly applies tax to bun + beef."""
    assert calculate_burger_price(["bun", "beef"]) == 8.47   # nosec B101

def test_load_last_count_missing(tmp_path) -> None:
    """Missing count file returns 0."""
    assert load_last_count(output_dir=str(tmp_path)) == 0   # nosec B101

def test_save_and_load_count(tmp_path) -> None:
    """Saving a burger updates the count file."""
    data = {"id": 5, "description": "test"}
    save_burger(data, output_dir=str(tmp_path))
    assert load_last_count(output_dir=str(tmp_path)) == 5   # nosec B101

def test_get_choice_valid(monkeypatch, capsys) -> None:
    """Valid input returns the choice without logging."""
    monkeypatch.setattr("builtins.input", lambda _: "mustard")
    choice = get_choice("Choose sauce", ("ketchup", "mustard"), "ketchup")
    assert choice == "mustard"   # nosec B101
    assert capsys.readouterr().out == ""   # nosec B101

def test_get_choice_invalid(monkeypatch, caplog) -> None:
    """Invalid input logs a defaulting message."""
    caplog.set_level(logging.INFO)
    monkeypatch.setattr("builtins.input", lambda _: "foo")
    choice = get_choice("Choose meat", ("beef", "chicken"), "beef")
    assert choice == "beef"   # nosec B101
    assert any("defaulting to 'beef'" in rec.getMessage().lower() for rec in caplog.records)   # nosec B101

def test_get_bun_default_and_custom(monkeypatch) -> None:
    """Empty bun defaults to 'regular', custom is respected."""
    monkeypatch.setattr("builtins.input", lambda _: "")
    assert get_bun() == "regular"   # nosec B101
    monkeypatch.setattr("builtins.input", lambda _: "sesame")
    assert get_bun() == "sesame"   # nosec B101

def test_get_meat_and_sauce(monkeypatch) -> None:
    """get_meat and get_sauce return valid selections."""
    monkeypatch.setattr("builtins.input", lambda _: "chicken")
    assert get_meat() == "chicken"   # nosec B101
    monkeypatch.setattr("builtins.input", lambda _: "mustard")
    assert get_sauce() == "mustard"   # nosec B101

def test_get_cheese_default_and_custom(monkeypatch) -> None:
    """Empty cheese defaults to 'cheddar', custom is respected."""
    monkeypatch.setattr("builtins.input", lambda _: "")
    assert get_cheese() == "cheddar"   # nosec B101
    monkeypatch.setattr("builtins.input", lambda _: "swiss")
    assert get_cheese() == "swiss"   # nosec B101

def test_get_order_timestamp_format() -> None:
    """Timestamp returned is ISO-formatted."""
    ts = get_order_timestamp()
    assert "T" in ts   # nosec B101
    datetime.fromisoformat(ts)

def test_assemble_burger_and_output(monkeypatch) -> None:
    """assemble_burger builds the correct dict and price."""
    inputs = iter(["sesame", "beef", "ketchup", "gouda"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    import developpement_logiciel.burger as burger_module
    monkeypatch.setattr(burger_module, "get_order_timestamp", lambda: "2025-06-13T12:00:00")
    result = assemble_burger(10)
    assert result["id"] == 10   # nosec B101
    assert result["timestamp"] == "2025-06-13T12:00:00"   # nosec B101
    assert result["description"] == "sesame bun + beef + ketchup + gouda cheese"   # nosec B101
    expected = calculate_burger_price(["bun", "beef", "sauce", "cheese"])
    assert result["price"] == expected   # nosec B101

def test_main_creates_files(tmp_path, monkeypatch) -> None:
    """main() writes burger.txt and burger_count.txt in OUTPUT_DIR."""
    import developpement_logiciel.burger as burger_module
    monkeypatch.setattr(burger_module, "OUTPUT_DIR", str(tmp_path))
    inputs = iter(["", "beef", "ketchup", ""])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    main()
    assert (tmp_path / "burger.txt").exists()   # nosec B101
    assert (tmp_path / "burger_count.txt").read_text() == "1"   # nosec B101
