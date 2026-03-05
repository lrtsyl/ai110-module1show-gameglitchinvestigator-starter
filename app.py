import random

import streamlit as st

from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    hint_message,
    parse_guess,
    update_score,
    validate_guess_in_range,
)
from storage_utils import update_high_score, load_high_score

HIGH_SCORE_PATH = "high_score.json"

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {"Easy": 6, "Normal": 8, "Hard": 5}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")


def reset_game():
    """Reset all game state for the current difficulty."""
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.guess_log = []  # Feature: visible guess history table
    # Important: clear the input using a callback button (on_click) to avoid StreamlitAPIException
    st.session_state[f"guess_input_{difficulty}"] = ""


# High score: load once per session
if "high_score" not in st.session_state:
    st.session_state.high_score = load_high_score(HIGH_SCORE_PATH)

# Initialize state on first load (or when difficulty changes).
if "difficulty" not in st.session_state:
    st.session_state.difficulty = difficulty
    reset_game()
elif st.session_state.difficulty != difficulty:
    # FIXME: Starter code broke here because difficulty changed without resetting state.
    st.session_state.difficulty = difficulty
    reset_game()

# Sidebar: High score display
st.sidebar.subheader("🏆 High Score")
hs = st.session_state.high_score
if hs:
    st.sidebar.success(
        f"{hs.get('best_score')} pts • {hs.get('best_attempts')} attempts • {hs.get('difficulty')}"
    )
else:
    st.sidebar.write("No high score yet. Win a game to set one!")

st.subheader("Make a guess")

attempts_left = max(attempt_limit - st.session_state.attempts, 0)
st.info(f"Guess a number between {low} and {high}. Attempts left: {attempts_left}")

raw_guess = st.text_input("Enter your guess:", key=f"guess_input_{difficulty}")

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    # FIX: callback reset avoids session_state widget-key mutation errors
    st.button("New Game 🔁", on_click=reset_game)
with col3:
    show_hint = st.checkbox("Show hint", value=True)

# Visible feature: Guess history table (not just in debug)
if st.session_state.get("guess_log"):
    st.subheader("Guess History")
    st.table(st.session_state.guess_log)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("Raw History:", st.session_state.history)

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    ok, guess_int, err = parse_guess(raw_guess)
    if not ok:
        st.error(err)
    else:
        in_range, range_err = validate_guess_in_range(guess_int, low, high)
        if not in_range:
            st.error(range_err)
        else:
            st.session_state.attempts += 1
            st.session_state.history.append(guess_int)

            outcome = check_guess(guess_int, st.session_state.secret)
            message = hint_message(outcome)

            # Log for the new UI table
            st.session_state.guess_log.append(
                {"attempt": st.session_state.attempts, "guess": guess_int, "result": outcome}
            )

            if show_hint:
                st.warning(message)

            st.session_state.score = update_score(
                current_score=st.session_state.score,
                outcome=outcome,
                attempt_number=st.session_state.attempts,
            )

            if outcome == "Win":
                st.balloons()
                st.session_state.status = "won"

                # Feature: persistent high score
                record, is_new = update_high_score(
                    new_score=st.session_state.score,
                    new_attempts=st.session_state.attempts,
                    difficulty=difficulty,
                    path=HIGH_SCORE_PATH,
                )
                st.session_state.high_score = record
                if is_new:
                    st.sidebar.success("New high score saved! 🏆")

                st.success(
                    f"You won! The secret was {st.session_state.secret}. "
                    f"Final score: {st.session_state.score}"
                )
            else:
                if st.session_state.attempts >= attempt_limit:
                    st.session_state.status = "lost"
                    st.error(
                        f"Out of attempts! The secret was {st.session_state.secret}. "
                        f"Score: {st.session_state.score}"
                    )

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
