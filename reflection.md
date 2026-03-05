# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

The first time I ran the game, it looked like a normal Streamlit guessing game with a difficulty selector, a score, and a “Developer Debug Info” panel showing the secret number. However, the game behavior didn’t match what the UI was telling me, so it felt unreliable even when I could see the secret.

Concrete bugs I noticed immediately:
- The hints were backwards: when my guess was higher than the secret, it would say “Too High” but then tell me “Go HIGHER!” (and the reverse for too low).
- The “New Game” button ignored the selected difficulty/range (it always generated a 1–100 secret), and the main prompt text always said “Guess a number between 1 and 100” even if the difficulty range was different.
- The score behaved strangely (for example, some wrong guesses could increase the score), and attempts didn’t feel consistent because invalid inputs could still affect attempts/history.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

- AI tools used:
  - GitHub Copilot Chat (in VS Code) for explaining code paths and generating pytest tests.
  - ChatGPT for proposing refactors and identifying likely Streamlit session_state issues.

- Example of a correct AI suggestion:
  - What the AI suggested: Move game logic out of `app.py` into `logic_utils.py` as pure functions (ex: `check_guess`, `parse_guess`) and fix the high/low comparison so guesses greater than the secret return "Too High" and guesses lower return "Too Low".
  - How I verified it: I added/updated pytest tests in `test_game_logic.py` (ex: `check_guess(60, 50) == "Too High"` and `check_guess(40, 50) == "Too Low"`), ran `pytest`, and confirmed the tests passed. I also ran the Streamlit app and verified the hint messages matched the debug secret.

- Example of an incorrect or misleading AI suggestion:
  - What the AI suggested: Clear the text input by setting `st.session_state["guess_input_Normal"] = ""` inside `reset_game()` and calling `reset_game()` directly when the “New Game” button is clicked.
  - Why it was misleading: Streamlit throws `StreamlitAPIException: ... cannot be modified after the widget with key ... is instantiated` if you modify a widget’s session_state key after it has already been created in that run.
  - How I verified it: I ran the app, clicked “New Game”, and reproduced the exception. I fixed it by changing the button to use a callback (`st.button("New Game 🔁", on_click=reset_game)`), then re-ran the app and confirmed the error was gone.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

- How I decided a bug was really fixed:
  I considered a bug fixed only when I could (1) reproduce the original bad behavior, (2) make a change that prevents it, and (3) verify the change both in the running Streamlit app and with automated tests (pytest). If the app “looked fine” but I couldn’t explain why, I didn’t count it as fixed yet.

- At least one test I ran and what it showed:
  I ran `pytest` after updating `logic_utils.py` and `tests/test_game_logic.py`. For example, I added tests like:
  - `check_guess(60, 50)` should return `"Too High"`
  - `check_guess(40, 50)` should return `"Too Low"`
  These tests proved the high/low logic was correct and stayed correct after refactoring.
  I also ran the Streamlit app (`python -m streamlit run app.py`) and used the debug panel showing the secret number to manually verify that the hint message matched the secret during gameplay.

- Did AI help with tests? How?
  Yes. AI (Copilot/ChatGPT) suggested writing small, deterministic pytest tests that directly target the bug (like “guess 60 when secret is 50 returns Too High”) instead of relying on random secrets. It also helped me think of input edge cases to test (like decimals or whitespace), and I verified the tests by running `pytest` and checking that failures matched the bug before the fix and passed after.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
