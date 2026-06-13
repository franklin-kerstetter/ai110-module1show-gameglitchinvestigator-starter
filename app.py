import json
import streamlit as st
from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)
from styles import get_theme_css
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

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

debug_mode = st.sidebar.toggle("🔧 Debug Mode", value=False)

if debug_mode:
    st.sidebar.write("Appearance: Hacker")
    appearance = "Hacker"
else:
    appearance = st.sidebar.selectbox(
        "Appearance",
        ["Classic", "Groovy", "Color-Blind"],
        index=0,
    )

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

initialize_game_state(difficulty, attempt_limit_map)

st.markdown(get_theme_css(appearance), unsafe_allow_html=True)

# Display win/loss results
if is_game_won():
    st.balloons()
    st.success(
        f"You won! The secret was {st.session_state.secret}. "
        f"Final score: {st.session_state.score}"
    )

if is_game_lost():
    st.error(
        f"Out of attempts! "
        f"The secret was {st.session_state.secret}. "
        f"Score: {st.session_state.score}"
    )

if debug_mode:
    col_main, col_debug = st.columns([2, 1])
else:
    col_main = st.columns([1])[0]
    col_debug = None

with col_main:
    st.subheader("Make a guess")

    st.info(
        f"Guess a number between 1 and 100. "
        f"Attempts left: {attempt_limit - st.session_state.attempts}"
    )

    hint = get_and_clear_hint()
    if hint:
        st.warning(hint)

    error = get_and_clear_error()
    if error:
        st.error(error)

    raw_guess = st.text_input(
        "Enter your guess:",
        key=f"guess_input_{difficulty}"
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        submit = st.button("Submit Guess 🚀", disabled=not can_submit(attempt_limit))
    with col2:
        new_game = st.button("New Game 🔁")
    with col3:
        show_hint = st.checkbox("Show hint", value=True)

    if new_game:
        reset_game()
        st.success("New game started.")
        st.rerun()
    
    if debug_mode and col_debug:
        with col_debug:
            st.subheader("🖥️ DEBUG")
            st.write("Secret:", st.session_state.secret)
            st.write("Attempts:", st.session_state.attempts)
            st.write("Score:", st.session_state.score)
            st.write("Difficulty:", difficulty)
            st.write("History:", json.dumps(st.session_state.history))

    if is_game_over():
        st.info("Start a new game to play again.")
        st.stop()

    if submit:
        ok, guess_int, err = parse_guess(raw_guess)

        if not ok:
            set_error(err)
        else:
            st.session_state.attempts += 1
            st.session_state.history.append(guess_int)

            if st.session_state.attempts % 2 == 0:
                secret = str(st.session_state.secret)
            else:
                secret = st.session_state.secret

            outcome, message = check_guess(guess_int, secret)

            if show_hint:
                set_hint(message)

            st.session_state.score = update_score(
                current_score=st.session_state.score,
                outcome=outcome,
                attempt_number=st.session_state.attempts,
            )

            if outcome == "Win":
                st.session_state.status = "won"
            elif st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"

        st.rerun()

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
