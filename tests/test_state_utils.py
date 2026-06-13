import pytest
from unittest.mock import MagicMock, patch
import sys
from pathlib import Path

# Mock streamlit before importing state_utils
sys.modules['streamlit'] = MagicMock()

from state_utils import (
    is_game_won,
    is_game_lost,
    is_game_over,
    can_submit,
    initialize_game_state,
    reset_game,
    get_and_clear_hint,
    set_hint,
    get_and_clear_error,
    set_error,
)


class SessionStateMock:
    """Mock for streamlit session_state that supports both attribute and dict-like access."""
    def __init__(self):
        self._data = {}

    def __setattr__(self, name, value):
        if name == '_data':
            object.__setattr__(self, name, value)
        else:
            self._data[name] = value

    def __getattr__(self, name):
        if name == '_data':
            return object.__getattribute__(self, name)
        return self._data.get(name)

    def __contains__(self, name):
        return name in self._data

    def get(self, name, default=None):
        return self._data.get(name, default)


@pytest.fixture
def mock_st():
    """Mock streamlit module with session_state."""
    with patch('state_utils.st') as mock:
        mock.session_state = SessionStateMock()
        yield mock


class TestGameStatusChecks:
    """Tests for game status check functions."""

    def test_is_game_won_true(self, mock_st):
        mock_st.session_state.status = "won"
        assert is_game_won() is True

    def test_is_game_won_false(self, mock_st):
        mock_st.session_state.status = "playing"
        assert is_game_won() is False

    def test_is_game_lost_true(self, mock_st):
        mock_st.session_state.status = "lost"
        assert is_game_lost() is True

    def test_is_game_lost_false(self, mock_st):
        mock_st.session_state.status = "playing"
        assert is_game_lost() is False

    @pytest.mark.parametrize(
        "status,expected",
        [
            ("playing", False),
            ("won", True),
            ("lost", True),
            ("unknown", True),
        ],
    )
    def test_is_game_over(self, mock_st, status, expected):
        mock_st.session_state.status = status
        assert is_game_over() is expected


class TestCanSubmit:
    """Tests for can_submit function."""

    def test_can_submit_game_playing_attempts_remaining(self, mock_st):
        mock_st.session_state.status = "playing"
        mock_st.session_state.attempts = 2
        assert can_submit(5) is True

    def test_can_submit_game_playing_no_attempts_remaining(self, mock_st):
        mock_st.session_state.status = "playing"
        mock_st.session_state.attempts = 5
        assert can_submit(5) is False

    def test_can_submit_game_won(self, mock_st):
        mock_st.session_state.status = "won"
        mock_st.session_state.attempts = 2
        assert can_submit(5) is False

    def test_can_submit_game_lost(self, mock_st):
        mock_st.session_state.status = "lost"
        mock_st.session_state.attempts = 3
        assert can_submit(5) is False

    def test_can_submit_exact_attempt_limit(self, mock_st):
        mock_st.session_state.status = "playing"
        mock_st.session_state.attempts = 4
        assert can_submit(5) is True

    def test_can_submit_zero_attempts_remaining(self, mock_st):
        mock_st.session_state.status = "playing"
        mock_st.session_state.attempts = 5
        assert can_submit(5) is False


class TestInitializeGameState:
    """Tests for initialize_game_state function."""

    @patch('state_utils.get_range_for_difficulty')
    @patch('state_utils.random.randint')
    def test_initialize_new_game(self, mock_randint, mock_get_range, mock_st):
        mock_st.session_state = MagicMock()
        mock_get_range.return_value = (1, 100)
        mock_randint.return_value = 42

        initialize_game_state("Normal", {})

        assert mock_st.session_state.difficulty == "Normal"
        assert mock_st.session_state.secret == 42
        assert mock_st.session_state.attempts == 0
        assert mock_st.session_state.score == 0
        assert mock_st.session_state.status == "playing"
        assert mock_st.session_state.history == []

    @patch('state_utils.get_range_for_difficulty')
    @patch('state_utils.random.randint')
    def test_initialize_same_difficulty_no_reset(self, mock_randint, mock_get_range, mock_st):
        mock_st.session_state.difficulty = 'Normal'
        mock_st.session_state.secret = 42
        mock_st.session_state.attempts = 3
        mock_st.session_state.score = 50
        mock_get_range.return_value = (1, 100)
        mock_randint.return_value = 99

        initialize_game_state("Normal", {})

        # Should not reset when same difficulty
        assert mock_st.session_state.secret == 42
        assert mock_st.session_state.attempts == 3

    @patch('state_utils.get_range_for_difficulty')
    @patch('state_utils.random.randint')
    def test_initialize_different_difficulty_resets(self, mock_randint, mock_get_range, mock_st):
        mock_st.session_state.difficulty = 'Easy'
        mock_st.session_state.secret = 42
        mock_st.session_state.attempts = 3
        mock_get_range.return_value = (1, 50)
        mock_randint.return_value = 25

        initialize_game_state("Hard", {})

        assert mock_st.session_state.difficulty == "Hard"
        assert mock_st.session_state.secret == 25
        assert mock_st.session_state.attempts == 0

    @pytest.mark.parametrize("difficulty", ["Easy", "Normal", "Hard"])
    @patch('state_utils.get_range_for_difficulty')
    @patch('state_utils.random.randint')
    def test_initialize_all_difficulties(self, mock_randint, mock_get_range, mock_st, difficulty):
        mock_get_range.return_value = (1, 100)
        mock_randint.return_value = 50

        initialize_game_state(difficulty, {})

        assert mock_st.session_state.difficulty == difficulty
        assert mock_st.session_state.status == "playing"


class TestResetGame:
    """Tests for reset_game function."""

    @patch('state_utils.get_range_for_difficulty')
    @patch('state_utils.random.randint')
    def test_reset_game_clears_attempts_and_history(self, mock_randint, mock_get_range, mock_st):
        mock_st.session_state.difficulty = 'Normal'
        mock_st.session_state.secret = 42
        mock_st.session_state.attempts = 5
        mock_st.session_state.history = [10, 20, 30]
        mock_st.session_state.score = 100
        mock_st.session_state.status = 'won'
        mock_get_range.return_value = (1, 100)
        mock_randint.return_value = 75

        reset_game()

        assert mock_st.session_state.attempts == 0
        assert mock_st.session_state.history == []
        assert mock_st.session_state.score == 0
        assert mock_st.session_state.status == "playing"
        assert mock_st.session_state.secret == 75

    @patch('state_utils.get_range_for_difficulty')
    @patch('state_utils.random.randint')
    def test_reset_game_preserves_difficulty(self, mock_randint, mock_get_range, mock_st):
        mock_st.session_state.difficulty = 'Hard'
        mock_st.session_state.secret = 42
        mock_get_range.return_value = (1, 50)
        mock_randint.return_value = 25

        reset_game()

        # Difficulty should be unchanged
        assert mock_st.session_state.difficulty == 'Hard'
        mock_get_range.assert_called_with('Hard')


class TestHintManagement:
    """Tests for hint storage and retrieval functions."""

    def test_set_hint_stores_message(self, mock_st):
        set_hint("Try a higher number!")

        assert mock_st.session_state.pending_hint == "Try a higher number!"

    def test_get_and_clear_hint_returns_hint(self, mock_st):
        mock_st.session_state.pending_hint = "Hint message"

        hint = get_and_clear_hint()

        assert hint == "Hint message"
        assert mock_st.session_state.pending_hint is None

    def test_get_and_clear_hint_no_hint(self, mock_st):
        mock_st.session_state = {}

        hint = get_and_clear_hint()

        assert hint is None

    def test_get_and_clear_hint_none_value(self, mock_st):
        mock_st.session_state.pending_hint = None

        hint = get_and_clear_hint()

        assert hint is None
        assert mock_st.session_state.pending_hint is None

    def test_hint_lifecycle(self, mock_st):
        """Test full hint storage and retrieval cycle."""
        # Store hint
        set_hint("Try lower!")
        assert mock_st.session_state.pending_hint == "Try lower!"

        # Retrieve hint
        hint = get_and_clear_hint()
        assert hint == "Try lower!"

        # Verify cleared
        assert mock_st.session_state.pending_hint is None

        # Second retrieval returns None
        hint = get_and_clear_hint()
        assert hint is None


class TestErrorManagement:
    """Tests for error storage and retrieval functions."""

    def test_set_error_stores_message(self, mock_st):
        set_error("That is not a number.")

        assert mock_st.session_state.pending_error == "That is not a number."

    def test_get_and_clear_error_returns_error(self, mock_st):
        mock_st.session_state.pending_error = "Invalid input"

        error = get_and_clear_error()

        assert error == "Invalid input"
        assert mock_st.session_state.pending_error is None

    def test_get_and_clear_error_no_error(self, mock_st):
        error = get_and_clear_error()

        assert error is None

    def test_get_and_clear_error_none_value(self, mock_st):
        mock_st.session_state.pending_error = None

        error = get_and_clear_error()

        assert error is None
        assert mock_st.session_state.pending_error is None

    def test_error_lifecycle(self, mock_st):
        """Test full error storage and retrieval cycle."""
        # Store error
        set_error("Enter a guess.")
        assert mock_st.session_state.pending_error == "Enter a guess."

        # Retrieve error
        error = get_and_clear_error()
        assert error == "Enter a guess."

        # Verify cleared
        assert mock_st.session_state.pending_error is None

        # Second retrieval returns None
        error = get_and_clear_error()
        assert error is None
