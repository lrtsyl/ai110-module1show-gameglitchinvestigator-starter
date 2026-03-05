from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional, Tuple


def load_high_score(path: str = "high_score.json") -> Optional[Dict[str, Any]]:
    """Load high score record from JSON. Returns None if missing/invalid."""
    p = Path(path)
    if not p.exists():
        return None
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return None
        # Basic shape validation
        if "best_score" not in data:
            return None
        return data
    except Exception:
        return None


def save_high_score(record: Dict[str, Any], path: str = "high_score.json") -> None:
    """Save high score record to JSON."""
    p = Path(path)
    p.write_text(json.dumps(record, indent=2), encoding="utf-8")


def update_high_score(
    new_score: int,
    new_attempts: int,
    difficulty: str,
    path: str = "high_score.json",
) -> Tuple[Dict[str, Any], bool]:
    """
    Update high score if new_score is better.

    Tie-breaker: fewer attempts wins if scores are equal.
    Returns: (record, is_new_high_score)
    """
    current = load_high_score(path) or {}

    cur_score = int(current.get("best_score", -1))
    cur_attempts = int(current.get("best_attempts", 10**9))

    is_better = (new_score > cur_score) or (new_score == cur_score and new_attempts < cur_attempts)
    if not is_better:
        # Keep existing, but ensure consistent structure
        record = {
            "best_score": cur_score,
            "best_attempts": cur_attempts,
            "difficulty": current.get("difficulty", "Unknown"),
        }
        return record, False

    record = {
        "best_score": int(new_score),
        "best_attempts": int(new_attempts),
        "difficulty": str(difficulty),
    }
    save_high_score(record, path)
    return record, True
