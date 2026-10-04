"""
BMI Calculator - Command-Line Application (Beginner Tier)

Calculates Body Mass Index (BMI) from weight (kg) and height (m),
classifies the result and displays it. Includes input validation
and a menu so the user can calculate again without restarting.
"""

# Sensible limits used only to catch obvious typing mistakes
# (for example, entering height in centimetres such as 170 instead of 1.70).
MAX_WEIGHT_KG = 500
MAX_HEIGHT_M = 3


# ---------------------------------------------------------------------------
# INPUT
# ---------------------------------------------------------------------------
def get_valid_number(prompt, label, unit, max_value, example):
    """
    Keep asking until the user enters a valid positive number.

    Rejects: non-numeric text, empty input, negative numbers, zero,
    and unrealistically large values.
    Returns the number as a float.
    """
    while True:
        user_text = input(prompt).strip()

        # 1. Check that the input is numeric
        try:
            value = float(user_text)
        except ValueError:
            print(f"  Error: '{user_text}' is not a number. "
                  f"Please enter {label} as a number (example: {example}).")
            continue

        # float("nan") and float("inf") are accepted by float(), so block them
        if value != value or value in (float("inf"), float("-inf")):
            print(f"  Error: '{user_text}' is not a valid number.")
            continue

        # 2. Check the number is not negative
        if value < 0:
            print(f"  Error: {label} cannot be negative. Please try again.")
            continue

        # 3. Check the number is not zero (zero height would divide by zero)
        if value == 0:
            print(f"  Error: {label} cannot be zero. Please enter a value "
                  f"greater than 0.")
            continue

        # 4. Check the number is realistic
        if value > max_value:
            print(f"  Error: {label} of {value} {unit} is unrealistic. "
                  f"Please enter a value up to {max_value} {unit}.")
            continue

        return value


def get_user_input():
    """Ask for weight (kg) and height (m); return them as a pair."""
    weight_kg = get_valid_number(
        "Enter your weight in kilograms (e.g. 70): ",
        "Weight", "kg", MAX_WEIGHT_KG, "65.5")
    height_m = get_valid_number(
        "Enter your height in meters (e.g. 1.75): ",
        "Height", "m", MAX_HEIGHT_M, "1.72")
    return weight_kg, height_m


# ---------------------------------------------------------------------------
# CALCULATION
# ---------------------------------------------------------------------------
def calculate_bmi(weight_kg, height_m):
    """
    Return BMI rounded to 2 decimal places.

    Formula: BMI = weight / (height ** 2)
    The value is rounded here so the number shown to the user and the
    number used for classification are always the same.
    """
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 2)


# ---------------------------------------------------------------------------
# CLASSIFICATION
# ---------------------------------------------------------------------------
def classify_bmi(bmi):
    """Return the BMI category name for a BMI value."""
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:            # 18.5 up to (but not including) 25
        return "Normal"
    elif bmi < 30:            # 25 up to (but not including) 30
        return "Overweight"
    else:                     # 30 and above
        return "Obese"


# ---------------------------------------------------------------------------
# OUTPUT
# ---------------------------------------------------------------------------
def display_result(weight_kg, height_m, bmi, category):
    """Print the result in a neat, readable format."""
    print()
    print("-" * 36)
    print("          YOUR BMI RESULT")
    print("-" * 36)
    print(f"  Weight   : {weight_kg} kg")
    print(f"  Height   : {height_m} m")
    print(f"  BMI      : {bmi:.2f}")
    print(f"  Category : {category}")
    print("-" * 36)
    print()


def display_heading():
    """Print the program title and short instructions."""
    print("=" * 36)
    print("         BMI CALCULATOR")
    print("=" * 36)
    print("Enter your weight (kg) and height (m)")
    print("to find your Body Mass Index.")
    print()


# ---------------------------------------------------------------------------
# MAIN PROGRAM
# ---------------------------------------------------------------------------
def main():
    """Run the menu loop so the user can calculate as many times as needed."""
    display_heading()

    while True:
        print("Menu:")
        print("  1. Calculate BMI")
        print("  2. Exit")
        choice = input("Enter your choice (1 or 2): ").strip()

        if choice == "1":
            weight_kg, height_m = get_user_input()
            bmi = calculate_bmi(weight_kg, height_m)
            category = classify_bmi(bmi)
            display_result(weight_kg, height_m, bmi, category)
        elif choice == "2":
            print("Thank you for using the BMI Calculator. Goodbye!")
            break
        else:
            # Invalid menu choice: explain and show the menu again
            print(f"  Invalid choice '{choice}'. Please enter 1 or 2.\n")


# Run main() only when this file is executed directly
if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C or Ctrl+D: exit politely instead of showing a traceback
        print("\nProgram closed. Goodbye!")
