# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [ ] Describe the game's purpose.
- [ ] Detail which bugs you found.
- [ ] Explain what fixes you applied.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

- Setup
1. Run the application
2. Enable the debugger toggle
3. Click the "New Game" button until the secret value is between 30 - 60
4. Disable debug mode

- Demo
1. User enters 22 in the "Enter your guess" field
2. User clicks the enter key on their keyboard
3. User clicks "Submit Guess"
4. Game responds with "Go HIGHER!"
5. User enters 88 in the "Enter your guess" field
6. User clicks the enter key on their keyboard
7. User clicks "Submit Guess"
8. Game responds with "Go LOWER!"
9. User guesses the secret number
10. Game responds with "Winner!", a balloon animation, & the user's score
11. User clicks the "New Game" button
12. Game resets the number of attempts, the score, and the history
13. User updates the appearance to `Groovy` 
13. User updates the appearance to `Color-Blind` 


## 🧪 Test Results

```
tests/test_game_logic.py ..........................                                                                                        [ 49%]
tests/test_state_utils.py ...........................                                                                                      [100%]

=============================================================== 53 passed in 0.04s ===============================================================
```

## 🚀 Stretch Features

> [X] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]

I added game styling options!
Users can now select from 3 different game appearances with a 4th "Hacker" style that enables when in debug mode.

Related to this, I hid the debug information behind a toggle in the left column rather than always present as an expander widget.
This toggle will enable the new styling and display the debug info in a column layout rather than as a long list.

As for relevant functions, there is an entirely new [styles.py](styles.py) file containing the CSS and style selection functions.