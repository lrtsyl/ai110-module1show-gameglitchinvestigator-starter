"""
Pure game-logic utilities for the Streamlit guessing game.

This module intentionally contains no Streamlit code so it can be unit tested with pytest.
"""

from __future__ import annotations

from typing import Optional, Tuple


def get_range_for_difficulty(difficulty: str) -> Tuple[int, int]:
    """
    Return (low, high) inclusive range for a given difficulty.

    Args:
        difficulty: One of "Easy", "Normal", "Hard".

    Returns:
        A tuple of inclusive bounds (low, high).
    """
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 200
    return 1, 100


def parse_guess(raw: Optional[str]) -> Tuple[bool, Optional[int], Optional[str]]:
    """
    Parse user input into an integer guess.

    Args:
        raw: Raw user input (string or None).

    Returns:
        (ok, guess, error_message)
        - ok is True when parsing succeeded.
        - guess is an int when ok is True, otherwise None.
        - error_message is a user-facing message when ok is False.

    Notes:
        - Only whole numbers are accepted (e.g., "12" is OK, "12.3" is rejected).
        - Leading/trailing whitespace is ignored.
    """
    if raw is None:
        return False, None, "Enter a guess."

    text = str(raw).strip()
    if text == "":
        return False, None, "Enter a guess."

    if "." in text:
        return False, None, "Please enter a whole number (no decimals)."

    try:
        value = int(text)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def validate_guess_in_range(guess: int, low: int, high: int) -> Tuple[bool, Optional[str]]:
    """
    Validate that a guess is within an inclusive range.

    Args:
        guess: The integer guess to validate.
        low: Inclusive lower bound.
        high: Inclusive upper bound.

    Returns:
        (ok, error_message)
    """
    if guess < low or guess > high:
        return False, f"Guess must be between {low} and {high}."
    return True, None


def check_guess(guess: int, secret: int) -> str:
    """
    Compare guess to secret and return an outcome string.

    Args:
        guess: Player guess.
        secret: Secret number.

    Returns:
        One of: "Win", "Too High", "Too Low".
    """
    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


def hint_message(outcome: str) -> str:
    """
    Return a user-facing hint message for an outcome.

    Args:
        outcome: Output from check_guess().

    Returns:
        A short string shown to the player.
    """
    if outcome == "Win":
        return "🎉 Correct!"
    if outcome == "Too High":
        return "📉 Go LOWER!"
    if outcome == "Too Low":
        return "📈 Go HIGHER!"
    return "Try again."


def update_score(current_score: int, outcome: str, attempt_number: int) -> int:
    """
    Update score based on outcome and attempt number.

    Scoring rules:
        - Wrong guess: -5 points (floored at 0)
        - Win: +max(10, 100 - 10*(attempt_number-1))

    Args:
        current_score: Current score value.
        outcome: "Win", "Too High", or "Too Low".
        attempt_number: 1-based attempt count.

    Returns:
        Updated score.
    """
    score = int(current_score)

    if outcome == "Win":
        points = 100 - 10 * (max(1, int(attempt_number)) - 1)
        return score + max(points, 10)

    if outcome in {"Too High", "Too Low"}:
        return max(score - 5, 0)

    return score
