"""
Pure game-logic utilities for the Streamlit guessing game.

This module intentionally contains no Streamlit code so it can be unit tested with pytest.
"""

from __future__ import annotations

from typing import Tuple


def get_range_for_difficulty(difficulty: str) -> Tuple[int, int]:
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        # Hard should actually be harder than Normal.
        return 1, 200
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)

    Notes:
      - Only whole numbers are accepted (e.g., "12" is OK, "12.3" is rejected).
      - Leading/trailing whitespace is ignored.
    """
    if raw is None:
        return False, None, "Enter a guess."

    text = str(raw).strip()
    if text == "":
        return False, None, "Enter a guess."

    # Reject decimals instead of silently truncating.
    if "." in text:
        return False, None, "Please enter a whole number (no decimals)."

    try:
        value = int(text)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def validate_guess_in_range(guess: int, low: int, high: int):
    """Validate that guess is within the inclusive [low, high] range."""
    if guess < low or guess > high:
        return False, f"Guess must be between {low} and {high}."
    return True, None


def check_guess(guess, secret) -> str:
    """
    Compare guess to secret and return an outcome string.

    Outcomes: "Win", "Too High", "Too Low"
    """
    # Keep comparisons numeric and deterministic.
    guess_i = int(guess)
    secret_i = int(secret)

    if guess_i == secret_i:
        return "Win"
    if guess_i > secret_i:
        return "Too High"
    return "Too Low"


def hint_message(outcome: str) -> str:
    """Return a user-facing hint message for an outcome."""
    if outcome == "Win":
        return "🎉 Correct!"
    if outcome == "Too High":
        # If your guess is too high, you should go lower.
        return "📉 Go LOWER!"
    if outcome == "Too Low":
        # If your guess is too low, you should go higher.
        return "📈 Go HIGHER!"
    return "Try again."


def update_score(current_score: int, outcome: str, attempt_number: int) -> int:
    """
    Update score based on outcome and attempt number.
    
    - Wrong guess: -5 points (floored at 0)
    - Win: +max(10, 100 - 10*(attempt_number-1))
    """
    score = int(current_score)

    if outcome == "Win":
        # attempt_number is 1-based (first valid guess => 1)
        points = 100 - 10 * (max(1, int(attempt_number)) - 1)
        points = max(points, 10)
        return score + points

    if outcome in {"Too High", "Too Low"}:
        return max(score - 5, 0)

    return score
