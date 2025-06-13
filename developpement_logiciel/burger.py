import os
from datetime import datetime

# Configuration
INGREDIENT_PRICES = {
    "bun": 2.0,
    "beef": 5.0,
    "chicken": 4.0,
    "cheese": 1.0,
    "tomato": 0.5,
    "lettuce": 0.5,
    "sauce": 0.3,
}
MEAT_OPTIONS = ("beef", "chicken")
SAUCE_OPTIONS = ("ketchup", "mustard")
TAX_RATE = 0.1  # 10%
TAX_ITERATIONS = 2
OUTPUT_DIR = "/tmp"


def get_order_timestamp() -> str:
    """Return the current timestamp in ISO format."""
    return datetime.now().isoformat()


def get_choice(prompt: str, options: tuple[str, ...], default: str) -> str:
    """Prompt user to choose from options, defaulting if invalid."""
    opts = "/".join(options)
    choice = input(f"{prompt} ({opts}): ").strip().lower()
    if choice not in options:
        print(f"Invalid choice, defaulting to '{default}'.")
        return default
    return choice


def get_bun() -> str:
    bun = input("What kind of bun would you like? ").strip()
    bun = bun or "regular"
    print(f"Selected bun: {bun}")
    return bun


def get_meat() -> str:
    meat = get_choice("Choose meat", MEAT_OPTIONS, "beef")
    print(f"Selected meat: {meat}")
    return meat


def get_sauce() -> str:
    sauce = get_choice("Choose sauce", SAUCE_OPTIONS, "ketchup")
    print(f"Selected sauce: {sauce}")
    return sauce


def get_cheese() -> str:
    cheese = input("What kind of cheese? ").strip()
    cheese = cheese or "cheddar"
    print(f"Selected cheese: {cheese}")
    return cheese


def calculate_burger_price(ingredients: list[str]) -> float:
    """Sum ingredient prices and apply compounded tax."""
    base = sum(INGREDIENT_PRICES.get(item, 0) for item in ingredients)
    total = base * ((1 + TAX_RATE) ** TAX_ITERATIONS)
    return round(total, 2)


def load_last_count(output_dir: str = OUTPUT_DIR) -> int:
    """Retrieve last burger count from file, or 0 if not found/invalid."""
    path = os.path.join(output_dir, "burger_count.txt")
    try:
        with open(path) as f:
            return int(f.read().strip())
    except (FileNotFoundError, ValueError):
        return 0


def save_burger(burger: dict[str, any], output_dir: str = OUTPUT_DIR) -> None:
    """Save burger description and ID to files."""
    os.makedirs(output_dir, exist_ok=True)
    desc_file = os.path.join(output_dir, "burger.txt")
    count_file = os.path.join(output_dir, "burger_count.txt")

    with open(desc_file, "w") as f:
        f.write(burger["description"])
    with open(count_file, "w") as f:
        f.write(str(burger["id"]))

    print(f"Burger saved to {desc_file}")


def assemble_burger(burger_id: int) -> dict[str, any]:
    """Gather selections, calculate price, and return burger data."""
    bun = get_bun()
    meat = get_meat()
    sauce = get_sauce()
    cheese = get_cheese()
    timestamp = get_order_timestamp()

    ingredients = ["bun", meat, "sauce", "cheese"]
    price = calculate_burger_price(ingredients)
    description = f"{bun} bun + {meat} + {sauce} + {cheese} cheese"

    return {
        "id": burger_id,
        "description": description,
        "price": price,
        "timestamp": timestamp,
    }


def main() -> None:
    print("Welcome to the optimized burger maker!")
    # Charger le compteur depuis OUTPUT_DIR
    current_id = load_last_count(output_dir=OUTPUT_DIR) + 1
    burger_data = assemble_burger(current_id)
    # Sauvegarder dans OUTPUT_DIR configurable (utile pour les tests)
    save_burger(burger_data, output_dir=OUTPUT_DIR)


if __name__ == "__main__":
    main()
