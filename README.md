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

> Describe the game's purpose.

From the application perspective, this game is a number guesser, guiding users to the secret application-selected random value.

From the CodePath learning perspective, this game's purpose was to act as a sandbox for working with AI tooling.
We had to run, debug, enhance, and automate a small codebase to achieve the desired functionality.
This acted as a small way of covering some of the main aspects of software engineering.

> Detail which bugs you found.

There were many bugs I found.
The most prominent ones are detailed in the [reflection: What was broken when you started?](reflection.md#1-what-was-broken-when-you-started) and were fixed.
In addition to these, I was particularly bothered by the late updating of the remaining submission count and the need to hit enter for submissions to log the updated value.

> Explain what fixes you applied.

Most of the fixes for the [reflection: What was broken when you started?](reflection.md#1-what-was-broken-when-you-started) bugs were minor.
For example, there was a state initialization line which set number of attempts to 1 rather than 0.
There was also code which always pulled the random number from a 1-100 range rather than the range from the difficulty that was updated to get the difficulty's range using `get_range_for_difficulty` in [logic_utils.py](logic_utils.py).

The more complicated refactoring came from fixing the lagging value updates.
This had to do with the widget rendering order, and, therefore, required reordering the widgets a bit and calling `rerun`.
Using the built-in `rerun` function was a gamechanger for my development, and having Claude opt for using it allowed me to learn of its existence.
Additionally, because I could see how Claude was using it, the behavior was much easier to understand than purely reading documentation.

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
14. User updates the appearance to `Color-Blind` 


## 🧪 Test Results

```
tests/test_game_logic.py ..........................                                                                                        [ 44%]
tests/test_state_utils.py ................................                                                                                 [100%]

=============================================================== 58 passed in 0.07s ===============================================================
```

## 🚀 Stretch Features

> [X] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]

I added game styling options!
Users can now select from 3 different game appearances with a 4th "Hacker" style that enables when in debug mode.

Related to this, I hid the debug information behind a toggle in the left column rather than always present as an expander widget.
This toggle will enable the new styling and display the debug info in a column layout rather than as a long list.

As for relevant functions, there is an entirely new [styles.py](styles.py) file containing the CSS and style selection functions.