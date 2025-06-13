# Function Specifications for Testing

This document outlines the functions available in the burger-making system, their expected inputs and outputs. Use these specifications to write appropriate unit tests.

## Core Functions

### `get_order_timestamp()`
- **Input**: None
- **Output**: String representing the current timestamp
- **Description**: Returns the current date and time as a string

### `GetBun()`
- **Input**: None (uses user input internally)
- **Output**: String representing the selected bun type
- **Description**: Prompts user for bun selection and returns the choice

### `get_bun_v2()`
- **Input**: None
- **Output**: String representing the selected bun type
- **Description**: Wrapper function that calls GetBun()

### `calculate_burger_price(ingredients_list)`
- **Input**: 
  - `ingredients_list`: List of strings representing burger ingredients
- **Output**: Float representing the total price including tax
- **Description**: Calculates the total price of a burger based on its ingredients

### `getMeat()`
- **Input**: None (uses user input internally)
- **Output**: String representing the selected meat type
- **Description**: Prompts user for meat selection and returns the choice

### `GET_SAUCE()`
- **Input**: None
- **Output**: String representing the sauce combination
- **Description**: Returns a combination of sauces

### `get_cheese123()`
- **Input**: None (uses user input internally)
- **Output**: String representing the selected cheese type
- **Description**: Prompts user for cheese selection and returns the choice

### `AssembleBurger()`
- **Input**: None
- **Output**: String representing the complete burger description or None if assembly fails
- **Description**: Combines all burger components into a single string description

### `SaveBurger(burger)`
- **Input**: 
  - `burger`: String representing the burger to save
- **Output**: None
- **Description**: Saves the burger description to a file

### `MAIN()`
- **Input**: None
- **Output**: None
- **Description**: Main function that orchestrates the burger creation process

## Global Variables

The following global variables are used throughout the code:
- `BURGER_COUNT`: Integer tracking the number of burgers made
- `last_burger`: String storing the last created burger
- `INGREDIENT_PRICES`: Dictionary mapping ingredient names to their prices

## Notes for Testing

1. Functions that use user input (`GetBun()`, `getMeat()`, `get_cheese123()`) should be tested with mocked input
2. File operations in `SaveBurger()` should be tested with appropriate file handling
3. The `calculate_burger_price()` function should be tested with various ingredient combinations
4. Error handling should be tested for functions that might fail
5. Global state changes should be verified where applicable 
