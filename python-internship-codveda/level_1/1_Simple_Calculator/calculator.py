"""
Simple Calculator - Python Development Internship
Codveda Technologies
Author: Suresh Das
Date: August 2026
"""

import sys
import time


def add(a, b):
    """Return the sum of two numbers."""
    return a + b


def subtract(a, b):
    """Return the difference of two numbers."""
    return a - b


def multiply(a, b):
    """Return the product of two numbers."""
    return a * b


def divide(a, b):
    """
    Return the quotient of two numbers.
    Handles division by zero with appropriate error message.
    """
    if b == 0:
        raise ValueError("Error: Division by zero is not allowed.")
    return a / b


def display_welcome():
    """Display welcome message and menu."""
    print("\n" + "=" * 50)
    print("          🧮 WELCOME TO SIMPLE CALCULATOR")
    print("=" * 50)
    print("\nSelect an operation:")
    print("  1. Addition (+)")
    print("  2. Subtraction (-)")
    print("  3. Multiplication (×)")
    print("  4. Division (÷)")
    print("  5. Exit")
    print("-" * 50)


def get_number(prompt):
    """Get a valid number input from the user."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("❌ Invalid input! Please enter a valid number.")


def get_operation():
    """Get a valid operation choice from the user."""
    while True:
        try:
            choice = int(input("\nEnter your choice (1-5): "))
            if 1 <= choice <= 5:
                return choice
            else:
                print("❌ Please enter a number between 1 and 5.")
        except ValueError:
            print("❌ Invalid input! Please enter a number.")


def perform_calculation(choice, num1, num2):
    """
    Perform the selected operation and return the result.
    """
    operations = {
        1: ("Addition", add),
        2: ("Subtraction", subtract),
        3: ("Multiplication", multiply),
        4: ("Division", divide)
    }
    
    op_name, op_func = operations[choice]
    
    try:
        result = op_func(num1, num2)
        return op_name, result, None
    except ValueError as e:
        return op_name, None, str(e)


def display_result(choice, op_name, num1, num2, result, error):
    """Display the calculation result or error message."""
    symbols = {1: "+", 2: "-", 3: "×", 4: "÷"}
    symbol = symbols.get(choice, "?")
    
    print("\n" + "-" * 40)
    if error:
        print(f"❌ {error}")
    else:
        print(f"📊 Result: {num1} {symbol} {num2} = {result}")
    print("-" * 40)


def calculator():
    """Main calculator function."""
    while True:
        display_welcome()
        choice = get_operation()
        
        if choice == 5:
            print("\n👋 Thank you for using the Simple Calculator!")
            print("   Stay tuned for more features! 🚀")
            time.sleep(1)
            break
        
        print("\n" + "-" * 40)
        print("📝 Enter your numbers:")
        print("-" * 40)
        
        num1 = get_number("  First number: ")
        num2 = get_number("  Second number: ")
        
        op_name, result, error = perform_calculation(choice, num1, num2)
        display_result(choice, op_name, num1, num2, result, error)
        
        # Ask if user wants to continue
        while True:
            cont = input("\n🔄 Do you want to perform another calculation? (y/n): ").lower()
            if cont in ['y', 'yes']:
                break
            elif cont in ['n', 'no']:
                print("\n👋 Thank you for using the Simple Calculator!")
                print("   🚀 Stay tuned for more features!")
                time.sleep(1)
                return
            else:
                print("❌ Please enter 'y' or 'n'.")


if __name__ == "__main__":
    calculator()