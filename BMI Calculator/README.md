# BMI Calculator

A beginner-level Python command-line application that calculates Body Mass Index (BMI) from weight and height and classifies the result.

## Features

- Takes weight in kilograms and height in metres.
- Calculates BMI using `weight / (height ** 2)`.
- Classifies BMI as:
  - Underweight: below 18.5
  - Normal: 18.5–24.9
  - Overweight: 25–29.9
  - Obese: 30 or above
- Displays BMI to 2 decimal places.
- Validates non-numeric, negative, zero, and unrealistic values.
- Allows multiple calculations without restarting.
- Handles invalid menu choices and exits gracefully.

## Technologies

- Python 3
- Python standard library

## Run

```bash
python bmi_calculator.py
```

No external packages are required.

## Project Structure

```text
BMI_Calculator/
├── bmi_calculator.py
└── README.md
```

## Concepts Used

Python input/output, variables, arithmetic, conditional statements, loops, functions, validation, and exception handling.
