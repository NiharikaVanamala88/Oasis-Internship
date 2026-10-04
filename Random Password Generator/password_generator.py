"""
Random Password Generator (Beginner Tier)

A command-line program that generates a random password based on the
user's chosen length and character types.

Note: this version uses the `random` module as required for the beginner
tier. It is NOT cryptographically secure (see README.md).
"""

import random
import string

MIN_LENGTH = 8      # minimum password length required by the task
MAX_LENGTH = 128    # sensible upper limit to avoid unreasonably long output
SYMBOLS = "!@#$%^&*"

# Menu number -> (name shown to user, characters belonging to that type)
CHARACTER_TYPES = {
    "1": ("Uppercase letters (A-Z)", string.ascii_uppercase),
    "2": ("Lowercase letters (a-z)", string.ascii_lowercase),
    "3": ("Numbers (0-9)", string.digits),
    "4": ("Symbols (" + SYMBOLS + ")", SYMBOLS),
}


def get_password_length():
    """Ask for the password length until a valid number is entered."""
    while True:
        text = input(f"Enter password length (minimum {MIN_LENGTH}): ").strip()

        try:
            length = int(text)  # fails for letters, decimals, empty text
        except ValueError:
            print("Error: please enter a whole number, e.g. 12.")
            continue

        if length < MIN_LENGTH:
            print(f"Error: length must be at least {MIN_LENGTH} characters.")
        elif length > MAX_LENGTH:
            print(f"Error: length must not be more than {MAX_LENGTH} characters.")
        else:
            return length


def get_character_options():
    """Ask which character types to use; return a list of character strings."""
    while True:
        print("\nChoose character types (select at least 2):")
        for number, (name, _) in CHARACTER_TYPES.items():
            print(f"  {number}. {name}")
        text = input("Enter numbers separated by commas (e.g. 1,3,4): ")

        # Accept both "1,2" and "1 2" by turning commas into spaces
        choices = text.replace(",", " ").split()

        # Reject anything that is not one of the menu options
        invalid = [c for c in choices if c not in CHARACTER_TYPES]
        if invalid:
            print(f"Error: invalid option(s): {', '.join(invalid)}. Use numbers 1-4 only.")
            continue

        unique_choices = sorted(set(choices))  # remove repeats like "1,1"
        if len(unique_choices) < 2:
            print("Error: you must select at least 2 different character types.")
            continue

        return [CHARACTER_TYPES[c][1] for c in unique_choices]


def generate_password(length, selected_sets):
    """Build a password of `length` using every selected character set."""
    # Step 1: guarantee one character from each selected type
    password_chars = [random.choice(chars) for chars in selected_sets]

    # Step 2: combine all selected types into one pool
    pool = "".join(selected_sets)

    # Step 3: fill the remaining positions from the pool
    while len(password_chars) < length:
        password_chars.append(random.choice(pool))

    # Step 4: shuffle so guaranteed characters are not always at the start
    random.shuffle(password_chars)

    return "".join(password_chars)


def ask_generate_another():
    """Ask 'y' or 'n' until a valid answer is given; return True for yes."""
    while True:
        answer = input("\nGenerate another password? (y/n): ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Error: please type 'y' for yes or 'n' for no.")


def main():
    """Run the program loop."""
    print("=== Random Password Generator ===")

    while True:
        length = get_password_length()
        selected_sets = get_character_options()
        password = generate_password(length, selected_sets)
        print(f"\nGenerated password: {password}")

        if not ask_generate_another():
            print("Goodbye!")
            break
        print()


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nProgram stopped. Goodbye!")
