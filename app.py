import time
import streamlit as st

st.set_page_config(
    page_title="Rest Reminder",
    page_icon="☕",
    layout="centered",
)

st.title("☕ Rest Reminder")
st.write("Stay focused, and remember to take breaks!")

# Initialize application state
if "running" not in st.session_state:
    st.session_state.running = False

if "next_break" not in st.session_state:
    st.session_state.next_break = None

if "work_minutes" not in st.session_state:
    st.session_state.work_minutes = 25

if "break_minutes" not in st.session_state:
    st.session_state.break_minutes = 5

st.subheader("Reminder settings")

work_minutes = st.number_input(
    "Work interval (minutes)",
    min_value=1,
    max_value=180,
    value=st.session_state.work_minutes,
    step=5,
)

break_minutes = st.number_input(
    "Break duration (minutes)",
    min_value=1,
    max_value=60,
    value=st.session_state.break_minutes,
    step=1,
)

st.session_state.work_minutes = work_minutes
st.session_state.break_minutes = break_minutes

col1, col2 = st.columns(2)

with col1:
    if st.button("▶ Start", use_container_width=True):
        st.session_state.running = True
        st.session_state.next_break = (
            time.time() + work_minutes * 60
        )

with col2:
    if st.button("⏸ Pause", use_container_width=True):
        st.session_state.running = False
        st.session_state.next_break = None

st.divider()


@st.fragment(run_every="1s")
def show_timer():
    if not st.session_state.running:
        st.info("Timer is paused. Press Start to begin.")
        return

    remaining = max(
        0,
        int(st.session_state.next_break - time.time()),
    )

    if remaining > 0:
        minutes, seconds = divmod(remaining, 60)
        st.subheader("Time until your next break")
        st.metric("Countdown", f"{minutes:02d}:{seconds:02d}")
        st.progress(
            1 - remaining / (st.session_state.work_minutes * 60)
        )
    else:
        st.warning(
            f"☕ Time to take a break! "
            f"Rest for {st.session_state.break_minutes} minutes."
        )
        st.write("Stretch, relax your eyes, or get some water.")

        if st.button("I've taken a break"):
            st.session_state.next_break = (
                time.time() + st.session_state.work_minutes * 60
            )
            st.rerun()


show_timer()
