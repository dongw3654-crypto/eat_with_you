import streamlit as st
import pandas as pd

# =====================
#conda env 启动
#启动提示
# streamlit run eat_with_you.py
# 读取 CSV
# =====================
df = pd.read_csv("outside_menu.csv")

st.set_page_config(
    page_title="今天和你一起吃什么",
    page_icon="🍽️",
    layout="centered"
)

st.markdown(
    "<h2 style='text-align:center; color:#C44569;'>🍽️ 今天和你一起吃什么</h2>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center; color:gray;'>预算是我们两个人这一顿的总花费 💕</p>",
    unsafe_allow_html=True
)

# =====================
# 预算（两个人总预算）
# =====================
total_budget = st.slider(
    "💰 今天这顿饭的总预算（两个人）",
    min_value=10,
    max_value=200,
    value=40,
    step=5
)

def pick_one():
    candidates = df[df["cost"] <= total_budget]

    if candidates.empty:
        return "那我们随便走走再看看吧 🥹"

    row = candidates.sample(1).iloc[0]
    return f"{row['restaurant']} · {row['dish']}  ｜ 共 ¥{row['cost']}"

# =====================
# 生成结果
# =====================
if st.button("💞 听你的，点一下"):
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🌤️ 午饭")
        st.success(pick_one())

    with col2:
        st.markdown("### 🌙 晚饭")
        st.success(pick_one())
