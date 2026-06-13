# AI Interactions Log

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| General edge case testing| Add automation around the central logic in app.py ensuring to cover edge cases | It basically built all the tests in the current file excluding the final large value case | No. I needed to add a follow-up to specify making the automation compliant with `pytest` | I wanted to see what test cases Claude would consider when guided with a general "edge case" prompt as compared with what I already had in mind. Overall, it aligned well, so I applied the suggested changes and cases. |
| Large value inputs | Add a test case for a large value user input | Test with `999999` as the user input | Yes | I noticed that this large value input case wasn't originally covered but was called out in the docs. It was worth adding for compeleteness. |

A lot of my automation was generated inline with the fix by prompting with something like "fix `problem` by `idea` and add or update automation."
As I reviewed every change Claude proposed along the way, I could better understand what was happening and have my own automation expectations.
If these expectations were not met, I'd ask for additional automation.

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
Add professional-grade docstrings to every function in @Game_Glitch_Investigator/logic_utils.py
```

After applying the docstrings given, I used the following prompt

```
Review my code for PEP 8 style compliance
```

**Linting output before:**

```
PEP 8 issues found:

Critical:

Missing return type hints — Lines 2, 26, 71, 116. Functions should declare return types:


def get_range_for_difficulty(difficulty: str) -> tuple:
def parse_guess(raw: str) -> tuple:
def check_guess(guess, secret) -> tuple:
def update_score(current_score: int, outcome: str, attempt_number: int) -> int:
Missing parameter type hints — Line 71. check_guess needs types:


def check_guess(guess: int, secret: int) -> tuple:
Blank line spacing — Line 24. Only one blank line between get_range_for_difficulty() and parse_guess(). PEP 8 requires two blank lines between top-level functions.

Minor:

Missing module docstring — File should start with a docstring describing the module's purpose.
```

**Changes applied:**

I agreed with and accepted all of Claude's proposed changes: adding a docstring to the top of [logic_utils.py](logic_utils.py), adding return type hints, adding parameter type hints, and normalizing the spacing between functions.