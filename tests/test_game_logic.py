from logic_utils import check_guess, parse_guess, update_score

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"

def test_parse_guess_rejects_decimals():
    ok, value, err = parse_guess("12.3")
    assert ok is False
    assert value is None
    assert err is not None

def test_parse_guess_strips_whitespace():
    ok, value, err = parse_guess("   42  ")
    assert ok is True
    assert value == 42
    assert err is None

def test_update_score_wrong_guess_decrements_and_floors_at_zero():
    assert update_score(3, "Too High", 1) == 0
    assert update_score(10, "Too Low", 1) == 5

def test_update_score_win_awards_more_on_earlier_attempts():
    assert update_score(0, "Win", 1) == 100
    assert update_score(0, "Win", 5) == 60
