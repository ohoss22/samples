import time
import streamlit as st

st.set_page_config(
    page_title="休息提醒",
    page_icon="☕",
    layout="centered",
)

MSG = "宝子，注意休息！起来活动一下，看看远处，喝点水吧。"

# 初始化状态
defaults = {
    "state": "idle",
    "elapsed": 0.0,
    "started_at": None,
    "duration": 10,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def toggle_timer():
    state = st.session_state.state

    if state in ("idle", "reminded"):
        st.session_state.elapsed = 0.0
        st.session_state.started_at = time.monotonic()
        st.session_state.state = "running"

    elif state == "running":
        st.session_state.elapsed += (
            time.monotonic() - st.session_state.started_at
        )
        st.session_state.started_at = None
        st.session_state.state = "paused"

    elif state == "paused":
        st.session_state.started_at = time.monotonic()
        st.session_state.state = "running"


def reset_timer():
    st.session_state.state = "idle"
    st.session_state.elapsed = 0.0
    st.session_state.started_at = None


st.title("☕ 休息提醒")
st.caption("认真工作，也别忘了照顾自己。")

st.divider()

st.subheader("⏱️ 计时设置")

# 计时运行时锁定时长，避免更改设置影响当前计时
if st.session_state.state in ("running", "paused"):
    st.number_input(
        "提醒间隔（秒）",
        min_value=1,
        max_value=3600,
        value=st.session_state.duration,
        disabled=True,
        help="请先重置计时，才能修改时长。",
    )
    st.caption(f"当前设置：{st.session_state.duration} 秒")
else:
    st.number_input(
        "提醒间隔（秒）",
        min_value=1,
        max_value=3600,
        step=1,
        key="duration",
        help="可设置 1～3600 秒，默认 10 秒。",
    )

st.divider()

# 操作按钮
state = st.session_state.state

button_labels = {
    "idle": "▶ 开始计时",
    "running": "⏸ 暂停计时",
    "paused": "▶ 继续计时",
    "reminded": "🔄 再来一轮",
}

col1, col2 = st.columns(2)

with col1:
    st.button(
        button_labels[state],
        on_click=toggle_timer,
        use_container_width=True,
        type="primary",
    )

with col2:
    st.button(
        "↺ 重置",
        on_click=reset_timer,
        use_container_width=True,
    )

st.divider()


@st.fragment(run_every=0.2)
def show_timer():
    state = st.session_state.state
    duration = st.session_state.duration

    if state == "running":
        elapsed = (
            st.session_state.elapsed
            + time.monotonic()
            - st.session_state.started_at
        )

        remaining = max(0.0, duration - elapsed)

        if remaining <= 0:
            st.session_state.state = "reminded"
            st.session_state.elapsed = duration
            st.session_state.started_at = None
            st.rerun()

        minutes, seconds = divmod(int(remaining), 60)

        st.subheader("距离休息提醒")
        st.metric("剩余时间", f"{minutes:02d}:{seconds:02d}")
        st.progress(min(elapsed / duration, 1.0))
        st.info("正在计时，请专注当前的事情。")

    elif state == "paused":
        remaining = max(
            0.0,
            duration - st.session_state.elapsed,
        )
        minutes, seconds = divmod(int(remaining), 60)

        st.subheader("计时已暂停")
        st.metric("剩余时间", f"{minutes:02d}:{seconds:02d}")
        st.progress(
            min(st.session_state.elapsed / duration, 1.0)
        )
        st.warning("点击“继续计时”即可继续。")

    elif state == "reminded":
        st.balloons()
        st.success("☕ 休息时间到！")
        st.warning(
            f"已计时 {duration} 秒。{MSG}"
        )

    else:
        st.subheader("准备好了吗？")
        st.metric("计时状态", "尚未开始")
        st.write(f"本轮将在 {duration} 秒后提醒你休息。")


show_timer()
