import os
import time
from datetime import datetime

# Pricing and tax configuration
INGREDIENT_PRICES = {
    "bun": 2.0,
    "beef": 5.0,
    "chicken": 4.0,
    "cheese": 1.0,
    "tomato": 0.5,
    "lettuce": 0.5,
    "sauce": 0.3,
}
TAX_RATE = 0.1  # 10% per iteration
TAX_ITERATIONS = 2  # Apply tax twice


def get_order_timestamp() -> str:
    """Return the current timestamp in ISO format."""
    return datetime.now().isoformat()


def get_bun() -> str:
    bun = input("What kind of bun would you like? ").strip()
    print(f"Selected bun: {bun}")
    return bun


def get_meat() -> str:
    meat = input("Enter the meat type (beef/chicken): ").strip().lower()
    if meat not in ("beef", "chicken"):
        print("Invalid choice, defaulting to 'beef'.")
        meat = "beef"
    print(f"Selected meat: {meat}")
    return meat


def get_sauce() -> str:
    options = ["ketchup", "mustard"]
    print(f"Available sauces: {', '.join(options)}")
    choice = input("Choose a sauce: ").strip().lower()
    if choice not in options:
        print("Invalid choice, defaulting to 'ketchup'.")
        choice = "ketchup"
    print(f"Selected sauce: {choice}")
    return choice


def get_cheese() -> str:
    cheese = input("What kind of cheese? ").strip()
    print(f"Selected cheese: {cheese}")
    return cheese


def calculate_burger_price(ingredients: list[str]) -> float:
    """Calculate total price including tax iterations."""
    base = sum(INGREDIENT_PRICES.get(item, 0) for item in ingredients)
    total = base
    for _ in range(TAX_ITERATIONS):
        total += total * TAX_RATE
    return round(total, 2)


def assemble_burger(burger_id: int) -> dict[str, any]:
    """Assemble burger components and return burger data."""
    bun = get_bun()
    meat = get_meat()
    sauce = get_sauce()
    cheese = get_cheese()
    timestamp = get_order_timestamp()
    price = calculate_burger_price(["bun", meat, "cheese", "sauce"])

    burger_desc = f"{bun} bun + {meat} + {sauce} + {cheese} cheese"
    return {
        "id": burger_id,
        "description": burger_desc,
        "price": price,
        "timestamp": timestamp,
    }


def save_burger(burger_data: dict[str, any], output_dir: str = "/tmp") -> None:
    """Save burger description and count to files."""
    os.makedirs(output_dir, exist_ok=True)
    burger_file = os.path.join(output_dir, "burger.txt")
    count_file = os.path.join(output_dir, "burger_count.txt")

    with open(burger_file, "w") as bf:
        bf.write(burger_data["description"])

    with open(count_file, "w") as cf:
        cf.write(str(burger_data["id"]))

    print(f"Burger saved to {burger_file}")


def load_last_count(output_dir: str = "/tmp") -> int:
    """Load last burger count, defaulting to 0 if missing or invalid."""
    count_file = os.path.join(output_dir, "burger_count.txt")
    try:
        with open(count_file) as cf:
            return int(cf.read().strip())
    except Exception:
        return 0


def main() -> None:
    print("Welcome to the best burger maker ever!")
    last_count = load_last_count()
    current_id = last_count + 1

    burger_data = assemble_burger(current_id)
    save_burger(burger_data)


if __name__ == "__main__":
    main()