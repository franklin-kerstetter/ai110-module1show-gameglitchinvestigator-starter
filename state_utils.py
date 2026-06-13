import random
import streamlit as st
from logic_utils import get_range_for_difficulty


def is_game_won():
    return st.session_state.status == "won"


def is_game_lost():
    return st.session_state.status == "lost"


def is_game_over():
    return st.session_state.status != "playing"


def can_submit(attempt_limit):
    return (
        st.session_state.status == "playing"
        and (attempt_limit - st.session_state.attempts) > 0
    )


def initialize_game_state(difficulty, attempt_limit_map):
    """Initialize or reset game state when difficulty changes."""
    if (
        "difficulty" not in st.session_state
        or st.session_state.difficulty != difficulty
    ):
        low, high = get_range_for_difficulty(difficulty)
        st.session_state.difficulty = difficulty
        st.session_state.secret = random.randint(low, high)
        st.session_state.attempts = 0
        st.session_state.score = 0
        st.session_state.status = "playing"
        st.session_state.history = []


def reset_game():
    """Reset game to play again."""
    st.session_state.attempts = 0
    st.session_state.history = []
    st.session_state.score = 0
    st.session_state.status = "playing"
    low, high = get_range_for_difficulty(st.session_state.difficulty)
    st.session_state.secret = random.randint(low, high)


def get_and_clear_hint():
    """Get stored hint message and clear it."""
    hint = st.session_state.get("pending_hint", None)
    if hint:
        st.session_state.pending_hint = None
    return hint


def set_hint(message):
    """Store hint message for display after rerun."""
    st.session_state.pending_hint = message


def get_and_clear_error():
    """Get stored error message and clear it."""
    error = st.session_state.get("pending_error", None)
    if error:
        st.session_state.pending_error = None
    return error


def set_error(message):
    """Store error message for display after rerun."""
    st.session_state.pending_error = message
