# Random Password Generator

A beginner-level Python command-line application that generates random passwords based on user-selected length and character types.

## Features

- Password length from 8 to 128 characters.
- Supports uppercase letters, lowercase letters, numbers, and symbols.
- Requires at least two character types.
- Guarantees at least one character from every selected type.
- Validates user input.
- Allows another password to be generated without restarting.
- Includes scenario-based tests.

## Technologies

- Python 3
- `random`
- `string`

## Run

```bash
python password_generator.py
```

To run the included tests:

```bash
python test_scenarios.py
```

No external packages are required.

## Project Structure

```text
Random_Password_Generator/
├── password_generator.py
├── test_scenarios.py
└── README.md
```

## Concepts Used

Random character selection, strings, lists/sets, functions, loops, conditional statements, input validation, and testing.

## Security Note

This beginner version uses Python's `random` module and is intended for learning. It is not a cryptographically secure password generator. For real security-sensitive passwords, Python's `secrets` module should be used.
