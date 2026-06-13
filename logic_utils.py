"""Game logic utilities for guess validation, scoring, and difficulty configuration."""

# FIX: AI Agent migrated code to utils file
def get_range_for_difficulty(difficulty: str) -> tuple:
    """
    Return the valid number range for a given difficulty level.

    Args:
        difficulty: The difficulty level as a string. Supported values are
            "Easy", "Normal", and "Hard". Defaults to "Normal" for unknown inputs.

    Returns:
        tuple: A tuple of (low, high) representing the inclusive range boundaries.
            - Easy: (1, 20)
            - Normal: (1, 100)
            - Hard: (1, 50)
            - Default: (1, 100)
    """
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


# FIX: AI Agent migrated code to utils file
def parse_guess(raw: str) -> tuple:
    """
    Parse and validate user input string into an integer guess.

    Handles None inputs, empty strings, decimal numbers (truncates to int),
    and non-numeric strings with appropriate error messages.

    Args:
        raw: The raw user input string to parse. Can be None or empty.

    Returns:
        tuple: A tuple of (ok, guess_int, error_message) where:
            - ok (bool): True if parsing succeeded, False otherwise.
            - guess_int (int | None): The parsed integer, or None if parsing failed.
            - error_message (str | None): User-friendly error message if parsing failed,
              or None if successful.

    Examples:
        >>> parse_guess("42")
        (True, 42, None)
        >>> parse_guess("3.7")
        (True, 3, None)
        >>> parse_guess("")
        (False, None, "Enter a guess.")
        >>> parse_guess("abc")
        (False, None, "That is not a number.")
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


# FIX: AI Agent migrated code to utils file
# FIX: AI Agent refactored hint messages
def check_guess(guess: int, secret: int) -> tuple:
    """
    Compare user guess against the secret number and provide feedback.

    Handles both numeric and string comparisons, attempting numeric comparison
    first before falling back to string comparison for type-mismatched inputs.
    Incorrect guesses show the guessed value for reference.

    Args:
        guess: The user's guess as an int or numeric value.
        secret: The secret number to guess against (int or comparable type).

    Returns:
        tuple: A tuple of (outcome, message) where:
            - outcome (str): One of "Win", "Too High", or "Too Low".
            - message (str): A user-friendly emoji-enhanced feedback message:
              * "🎉 Correct!" for Win
              * "📉 Go LOWER than {guess}!" for Too High
              * "📈 Go HIGHER than {guess}!" for Too Low

    Examples:
        >>> check_guess(42, 42)
        ("Win", "🎉 Correct!")
        >>> check_guess(50, 42)
        ("Too High", "📉 Go LOWER than 50!")
        >>> check_guess(30, 42)
        ("Too Low", "📈 Go HIGHER than 30!")
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    try:
        if guess > secret:
            return "Too High", f"📉 Go LOWER than {guess}!"
        else:
            return "Too Low", f"📈 Go HIGHER than {guess}!"
    except TypeError:
        g = str(guess)
        if g == secret:
            return "Win", "🎉 Correct!"
        if g > secret:
            return "Too High", f"📉 Go LOWER than {g}!"
        else:
            return "Too Low", f"📈 Go HIGHER than {g}!"


def update_score(current_score: int, outcome: str, attempt_number: int) -> int:
    """
    Calculate and return the updated score based on game outcome and attempt number.

    Scoring rules:
    - Win: Award 100 - 10*(attempt_number + 1) points, minimum 10 points.
    - Too High: Award 5 points on even attempts, deduct 5 on odd attempts.
    - Too Low: Always deduct 5 points.
    - Other outcomes: No score change.

    Args:
        current_score: The player's current score before this attempt (int).
        outcome: The result of the guess comparison. Expected values: "Win",
            "Too High", "Too Low", or other (no change).
        attempt_number: Zero-indexed attempt count (0 for first guess, 1 for second, etc.).

    Returns:
        int: The updated total score after applying the outcome-based adjustment.

    Examples:
        >>> update_score(0, "Win", 0)
        90
        >>> update_score(100, "Win", 5)
        45
        >>> update_score(100, "Too High", 0)
        105
        >>> update_score(100, "Too High", 1)
        95
        >>> update_score(100, "Too Low", 2)
        95
    """
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
