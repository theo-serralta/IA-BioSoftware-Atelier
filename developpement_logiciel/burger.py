import logging
import os
import tempfile
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
TAX_RATE = 0.1
TAX_ITERATIONS = 2
OUTPUT_DIR = tempfile.gettempdir()

def get_order_timestamp() -> str:
    """Return current timestamp in ISO 8601 format."""
    return datetime.now().isoformat()

def get_choice(prompt: str, options: tuple[str, ...], default: str) -> str:
    """Prompt user for choice; return default if invalid."""
    opts = "/".join(options)
    choice = input(f"{prompt} ({opts}): ").strip().lower()
    if choice not in options:
        logger.info("Invalid choice '%s', defaulting to '%s'", choice, default)
        return default
    return choice

def get_bun() -> str:
    """Prompt for bun type, defaulting to 'regular'."""
    bun = input("What kind of bun would you like? ").strip() or "regular"
    logger.info("Selected bun: %s", bun)
    return bun

def get_meat() -> str:
    """Prompt for meat selection."""
    meat = get_choice("Choose meat", MEAT_OPTIONS, "beef")
    logger.info("Selected meat: %s", meat)
    return meat

def get_sauce() -> str:
    """Prompt for sauce selection."""
    sauce = get_choice("Choose sauce", SAUCE_OPTIONS, "ketchup")
    logger.info("Selected sauce: %s", sauce)
    return sauce

def get_cheese() -> str:
    """Prompt for cheese type, defaulting to 'cheddar'."""
    cheese = input("What kind of cheese? ").strip() or "cheddar"
    logger.info("Selected cheese: %s", cheese)
    return cheese

def calculate_burger_price(ingredients: list[str]) -> float:
    """Calculate total price including compounded tax."""
    base = sum(INGREDIENT_PRICES.get(item, 0) for item in ingredients)
    total = base * ((1 + TAX_RATE) ** TAX_ITERATIONS)
    return round(total, 2)

def load_last_count(output_dir: str = OUTPUT_DIR) -> int:
    """Load last burger count from file or return 0."""
    path = os.path.join(output_dir, "burger_count.txt")
    try:
        with open(path) as f:
            return int(f.read().strip())
    except (FileNotFoundError, ValueError):
        return 0

def save_burger(burger: dict[str, any], output_dir: str = OUTPUT_DIR) -> None:
    """Save burger description and ID to files."""
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, "burger.txt"), "w") as f:
        f.write(burger["description"])
    with open(os.path.join(output_dir, "burger_count.txt"), "w") as f:
        f.write(str(burger["id"]))

def assemble_burger(burger_id: int) -> dict[str, any]:
    """Assemble burger components and return metadata."""
    bun = get_bun()
    meat = get_meat()
    sauce = get_sauce()
    cheese = get_cheese()
    timestamp = get_order_timestamp()
    ingredients = ["bun", meat, "sauce", "cheese"]
    price = calculate_burger_price(ingredients)
    description = f"{bun} bun + {meat} + {sauce} + {cheese} cheese"
    return {"id": burger_id, "description": description, "price": price, "timestamp": timestamp}

def main() -> None:
    """Assemble and save a burger."""
    current_id = load_last_count(output_dir=OUTPUT_DIR) + 1
    burger_data = assemble_burger(current_id)
    save_burger(burger_data, output_dir=OUTPUT_DIR)

if __name__ == "__main__":
    main()
