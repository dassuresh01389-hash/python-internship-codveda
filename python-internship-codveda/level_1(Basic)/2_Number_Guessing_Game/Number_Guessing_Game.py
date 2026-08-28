"""
Number Guessing Game - Internship Submission
Author: Suresh Das
Date: 2026-08-28
Description: A CLI-based number guessing game with configurable difficulty,
             input validation, replayability, and unit test support.
"""

import random
import sys
from typing import Optional

# Configuration
DEFAULT_MIN = 1
DEFAULT_MAX = 100
DEFAULT_ATTEMPTS = 10


class GuessingGame:
    """Encapsulates the game logic and state."""

    def __init__(self, min_num: int = DEFAULT_MIN, max_num: int = DEFAULT_MAX,
                 max_attempts: int = DEFAULT_ATTEMPTS):
        self.min_num = min_num
        self.max_num = max_num
        self.max_attempts = max_attempts
        self.secret: Optional[int] = None
        self.attempts_used = 0
        self.game_over = False

    def reset(self) -> None:
        """Reset the game state with a new random secret."""
        self.secret = random.randint(self.min_num, self.max_num)
        self.attempts_used = 0
        self.game_over = False

    def make_guess(self, guess: int) -> str:
        """
        Process a guess and return feedback.
        Raises:
            ValueError: If guess is out of range or game is over.
        """
        if self.game_over:
            raise ValueError("Game is already over. Please reset.")
        if not (self.min_num <= guess <= self.max_num):
            raise ValueError(f"Guess must be between {self.min_num} and {self.max_num}.")

        self.attempts_used += 1

        if guess == self.secret:
            self.game_over = True
            return f"🎉 Correct! You got it in {self.attempts_used} tries."
        elif guess < self.secret:
            return "📈 Too low!"
        else:
            return "📉 Too high!"

    def is_won(self) -> bool:
        return self.game_over and self.attempts_used <= self.max_attempts

    def is_lost(self) -> bool:
        return self.attempts_used >= self.max_attempts and not self.game_over

    def get_remaining_attempts(self) -> int:
        return self.max_attempts - self.attempts_used


def run_cli() -> None:
    """Command-line interface for the game."""
    print("\n🎯 Welcome to the Number Guessing Game!")
    print("=" * 40)

    # Difficulty selection (extra polish)
    difficulties = {
        "1": (1, 50, 8, "Easy"),
        "2": (1, 100, 10, "Medium"),
        "3": (1, 200, 7, "Hard"),
    }
    print("Select difficulty:")
    for key, (mn, mx, att, name) in difficulties.items():
        print(f"  {key}. {name} (1-{mx}, {att} attempts)")
    choice = input("Enter 1, 2, or 3 (default 2): ").strip() or "2"
    min_n, max_n, max_att = difficulties.get(choice, difficulties["2"])[:3]

    game = GuessingGame(min_n, max_n, max_att)
    game.reset()

    print(f"\nI'm thinking of a number between {min_n} and {max_n}.")
    print(f"You have {max_att} attempts. Let's begin!\n")

    while not game.game_over:
        remaining = game.get_remaining_attempts()
        if remaining <= 0:
            print(f"\n😞 Out of attempts! The number was {game.secret}.")
            break

        # Input with robust validation
        try:
            raw = input(f"[Attempts left: {remaining}] Enter your guess: ").strip()
            if raw.lower() in ("q", "quit", "exit"):
                print("👋 Thanks for playing! Goodbye.")
                return
            guess = int(raw)
            feedback = game.make_guess(guess)
            print(feedback)

            if game.is_won():
                print("🏆 You win! Amazing work.")
                break
        except ValueError as e:
            print(f"⚠️ {e}")

    # Replay prompt
    replay = input("\nPlay again? (y/n): ").strip().lower()
    if replay == "y":
        run_cli()
    else:
        print("Thanks for playing! 👋")


# ---------- Unit Test (run with: pytest or python -m doctest) ----------
def test_game_logic() -> None:
    """Simple unit test to verify game logic (run this manually or with pytest)."""
    game = GuessingGame(1, 10, 3)
    game.secret = 5  # Force known secret for testing

    assert game.make_guess(3) == "📈 Too low!"
    assert game.make_guess(7) == "📉 Too high!"
    assert game.make_guess(5) == "🎉 Correct! You got it in 3 tries."
    assert game.is_won() is True
    print("✅ All logic tests passed.")


if __name__ == "__main__":
    # Uncomment the line below to run the unit test instead of the game
    # test_game_logic()
    run_cli()