"""
🍽️ 今天和你一起吃什么
一个基于 Streamlit 的两人用餐随机选择器
根据预算随机推荐午饭和晚饭，总价不超预算
"""

import random
import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path

# ============================================================
# 页面配置
# ============================================================
st.set_page_config(
    page_title="今天和你一起吃什么",
    page_icon="🍽️",
    layout="centered"
)

# ============================================================
# 数据加载
# ============================================================
@st.cache_data
def load_menu():
    csv_path = Path(__file__).parent / "outside_menu.csv"
    df = pd.read_csv(csv_path)
    df = df.dropna(how="all")
    df = df.dropna(subset=["restaurant", "dish", "cost"])
    df["cost"] = df["cost"].astype(float)
    df["unique_id"] = df["restaurant"] + " | " + df["dish"]
    return df

df = load_menu()

# ============================================================
# 配色与常量
# ============================================================
COLORS = {
    "primary": "#C44569",
    "secondary": "#E66767",
    "lunch_bg_start": "#FFF5E1",
    "lunch_bg_end": "#FFECD2",
    "lunch_border": "#F6C76D",
    "dinner_bg_start": "#F0E6FF",
    "dinner_bg_end": "#E8D5F5",
    "dinner_border": "#B794F4",
    "page_bg_start": "#FFF5F5",
    "page_bg_end": "#FFF0E6",
    "text_primary": "#2D3436",
    "text_secondary": "#636E72",
    "price": "#C44569",
    "success": "#00B894",
    "warning": "#FDCB6E",
    "danger": "#E66767",
}

FOOD_EMOJI_MAP = {
    "汉堡": "🍔", "pizza": "🍕", "麻婆豆腐": "🥘",
    "石锅拌饭": "🍚", "八宝粥": "🥣", "麻辣香锅": "🌶️",
    "麻辣烫": "🍜", "面条": "🍝", "寿司": "🍣",
    "烤鱼": "🐟", "天津包子": "🥟", "米线": "🍲",
    "糁汤": "🥘", "鸡公煲": "🐔", "砂锅": "🥘",
    "牛肉汤": "🍖", "羊肉汤": "🐑", "炒香鸡": "🍗",
    "卤肉拌面": "🍜", "安徽板面": "🍜", "有福面": "🍜",
    "菜米饭": "🍚", "三餐简餐": "🍱", "鱼先生": "🐟",
    "洪兴砂锅": "🥘", "鸡汤面": "🍜",
}
DEFAULT_EMOJI = "🍽️"

# ============================================================
# CSS 样式注入
# ============================================================
def inject_custom_css():
    st.markdown(f"""
    <style>
    /* === 页面背景渐变 === */
    .stApp {{
        background: linear-gradient(135deg, {COLORS["page_bg_start"]} 0%, {COLORS["page_bg_end"]} 100%);
    }}

    /* === 卡片通用样式 === */
    .meal-card {{
        border-radius: 16px;
        padding: 28px 20px 24px;
        margin: 8px 0;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.07);
        transition: transform 0.25s, box-shadow 0.25s;
        min-height: 220px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }}
    .meal-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
    }}

    /* === 午饭卡片 === */
    .lunch-card {{
        background: linear-gradient(180deg, {COLORS["lunch_bg_start"]}, {COLORS["lunch_bg_end"]});
        border-left: 5px solid {COLORS["lunch_border"]};
    }}

    /* === 晚饭卡片 === */
    .dinner-card {{
        background: linear-gradient(180deg, {COLORS["dinner_bg_start"]}, {COLORS["dinner_bg_end"]});
        border-left: 5px solid {COLORS["dinner_border"]};
    }}

    /* === 卡片内文字 === */
    .meal-emoji {{
        font-size: 2.8em;
        margin-bottom: 8px;
    }}
    .meal-restaurant {{
        font-size: 1.3em;
        font-weight: 700;
        color: {COLORS["text_primary"]};
        margin-bottom: 4px;
    }}
    .meal-dish {{
        font-size: 1.05em;
        color: {COLORS["text_secondary"]};
        margin-bottom: 10px;
    }}
    .meal-price {{
        font-size: 1.5em;
        font-weight: 700;
        color: {COLORS["price"]};
    }}

    /* === 合计栏 === */
    .total-bar {{
        background: white;
        border-radius: 12px;
        padding: 16px 24px;
        text-align: center;
        font-size: 1.15em;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin: 20px 0;
        font-weight: 600;
    }}
    .total-bar.over-budget {{
        border: 2px solid {COLORS["danger"]};
        background: #FFF0F0;
        color: {COLORS["danger"]};
    }}
    .total-bar.in-budget {{
        border: 2px solid {COLORS["success"]};
        background: #F0FFF5;
        color: {COLORS["success"]};
    }}

    /* === 预算控制容器 === */
    .budget-section {{
        background: white;
        border-radius: 16px;
        padding: 20px 24px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }}

    /* === 按钮美化 === */
    div.stButton > button:first-child {{
        background: linear-gradient(135deg, {COLORS["primary"]}, {COLORS["secondary"]});
        color: white !important;
        border: none;
        border-radius: 25px;
        padding: 10px 28px;
        font-size: 1.05em;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(196, 69, 105, 0.3);
        width: 100%;
    }}
    div.stButton > button:first-child:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 22px rgba(196, 69, 105, 0.45);
    }}

    /* === 次要按钮（再试一次） === */
    .retry-btn div.stButton > button:first-child {{
        background: white;
        color: {COLORS["primary"]} !important;
        border: 2px solid {COLORS["primary"]};
        box-shadow: 0 2px 8px rgba(196, 69, 105, 0.12);
    }}

    /* === 历史记录样式 === */
    .history-item {{
        background: white;
        border-radius: 10px;
        padding: 10px 18px;
        margin: 6px 0;
        border-left: 4px solid {COLORS["primary"]};
        font-size: 0.95em;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    }}
    .history-item .time {{
        color: {COLORS["text_secondary"]};
        font-size: 0.8em;
    }}

    /* === 页脚 === */
    .footer {{
        text-align: center;
        color: {COLORS["text_secondary"]};
        font-size: 0.85em;
        margin-top: 40px;
        padding: 20px 0;
        opacity: 0.7;
    }}
    </style>
    """, unsafe_allow_html=True)

inject_custom_css()

# ============================================================
# 核心算法：预算约束下的组合抽取
# ============================================================
def pick_combination(df, total_budget):
    """
    从菜单中抽取两道不同菜品的组合。
    CSV 中存的是单价（每人），实际花销 = 单价 × 2 人。
    约束：lunch单价×2 + dinner单价×2 ≤ total_budget
    返回 (lunch_row, dinner_row) 或 (None, None)。
    """
    affordable = df[df["cost"] * 2 <= total_budget].copy()

    if len(affordable) < 2:
        return None, None

    # 生成所有合法组合（按两人总价计算）
    pairs = []
    indices = affordable.index.tolist()
    for i in range(len(indices)):
        for j in range(len(indices)):
            if i == j:
                continue
            cost_i = affordable.loc[indices[i], "cost"] * 2  # 两人总价
            cost_j = affordable.loc[indices[j], "cost"] * 2
            if cost_i + cost_j <= total_budget:
                pairs.append((indices[i], indices[j]))

    if not pairs:
        return None, None

    # 随机选一组
    lunch_idx, dinner_idx = random.choice(pairs)

    return df.loc[lunch_idx], df.loc[dinner_idx]


def get_food_emoji(dish_name):
    """根据菜名匹配对应食物 emoji"""
    for key, emoji in FOOD_EMOJI_MAP.items():
        if key in dish_name:
            return emoji
    return DEFAULT_EMOJI


def fmt_price(cost):
    """格式化单价显示"""
    if cost == int(cost):
        return f"¥{int(cost)}"
    else:
        return f"¥{cost:.1f}"

def render_meal_card(label, row, emoji):
    """渲染单个菜品卡片 HTML，显示单价及两人总价"""
    card_class = "lunch-card" if label == "lunch" else "dinner-card"
    restaurant = row["restaurant"]
    dish = row["dish"]
    cost_per = row["cost"]        # 单价
    cost_two = cost_per * 2       # 两人总价

    return f"""
    <div class="meal-card {card_class}">
        <div class="meal-emoji">{emoji}</div>
        <div class="meal-restaurant">🏠 {restaurant}</div>
        <div class="meal-dish">{dish}</div>
        <div class="meal-price">{fmt_price(cost_per)}<span style="font-size:0.6em;color:#636E72;"> /人</span></div>
        <div style="font-size:0.85em;color:#636E72;margin-top:2px;">
            👫 两人共 {fmt_price(cost_two)}
        </div>
    </div>
    """


# ============================================================
# 会话状态初始化
# ============================================================
if "history" not in st.session_state:
    st.session_state.history = []
if "current_pick" not in st.session_state:
    st.session_state.current_pick = None
if "locked_budget" not in st.session_state:
    st.session_state.locked_budget = None

# ============================================================
# 标题区域
# ============================================================
st.markdown(
    "<h2 style='text-align:center; color:#C44569; margin-bottom:4px;'>"
    "🍽️ 今天和你一起吃什么</h2>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align:center; color:gray; margin-bottom:20px;'>"
    "预算是我们两个人这一顿的总花费 💕</p>",
    unsafe_allow_html=True
)

# ============================================================
# 页面标签页
# ============================================================
tab1, tab2 = st.tabs(["🎲 随机选择", "📝 菜谱管理"])

# ==================== Tab 1：随机选择 ====================
with tab1:
    # 预算控制区域
    st.markdown('<div class="budget-section">', unsafe_allow_html=True)

    total_budget = st.slider(
        "💰 今天两顿饭的总预算（两人 × 午饭 + 两人 × 晚饭）",
        min_value=10,
        max_value=100,
        value=40,
        step=5,
        key="budget_slider"
    )

    # 预算提示（按每人每顿最低 ¥5 估算，两顿×两人 = 最低 ¥20）
    if total_budget < 20:
        st.warning("💡 预算比较紧哦，每人每顿不到 ¥5，可能不太够～")
    elif total_budget < 40:
        st.info("💡 预算适中，每人每顿 ¥5~10，简单温馨～")
    elif total_budget < 70:
        st.info("💡 预算充裕，可以吃得很丰盛啦 ✨")
    else:
        st.info("💡 预算非常充足，大餐走起！🎉")

    # 如果滑块调整了，清除上次的抽取结果
    if st.session_state.locked_budget is not None and total_budget != st.session_state.locked_budget:
        st.session_state.current_pick = None
        st.session_state.locked_budget = None

    st.markdown('</div>', unsafe_allow_html=True)

    # 按钮区域
    col_btn1, col_btn2 = st.columns([1, 1])

    with col_btn1:
        if st.button("💞 听你的，点一下", use_container_width=True):
            st.session_state.locked_budget = total_budget
            lunch, dinner = pick_combination(df, total_budget)
            if lunch is not None:
                st.session_state.current_pick = (lunch, dinner)
                now = datetime.now().strftime("%H:%M")
                st.session_state.history.insert(0, {
                    "time": now,
                    "lunch": f"{lunch['restaurant']}·{lunch['dish']}",
                    "dinner": f"{dinner['restaurant']}·{dinner['dish']}",
                    "total": (lunch["cost"] + dinner["cost"]) * 2,
                    "budget": total_budget,
                })
                if len(st.session_state.history) > 10:
                    st.session_state.history = st.session_state.history[:10]
            else:
                st.session_state.current_pick = None

    with col_btn2:
        if st.session_state.current_pick is not None:
            st.markdown('<div class="retry-btn">', unsafe_allow_html=True)
            if st.button("🔄 再试一次", use_container_width=True):
                lunch, dinner = pick_combination(df, st.session_state.locked_budget)
                if lunch is not None:
                    st.session_state.current_pick = (lunch, dinner)
                    now = datetime.now().strftime("%H:%M")
                    st.session_state.history.insert(0, {
                        "time": now,
                        "lunch": f"{lunch['restaurant']}·{lunch['dish']}",
                        "dinner": f"{dinner['restaurant']}·{dinner['dish']}",
                        "total": (lunch["cost"] + dinner["cost"]) * 2,
                        "budget": st.session_state.locked_budget,
                    })
                    if len(st.session_state.history) > 10:
                        st.session_state.history = st.session_state.history[:10]
            st.markdown('</div>', unsafe_allow_html=True)

    # 结果展示区域
    if st.session_state.current_pick is not None:
        lunch, dinner = st.session_state.current_pick
        budget_used = st.session_state.locked_budget

        st.markdown("---")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 🌤️ 午饭")
            emoji = get_food_emoji(lunch["dish"])
            st.markdown(render_meal_card("lunch", lunch, emoji), unsafe_allow_html=True)

        with col2:
            st.markdown("### 🌙 晚饭")
            emoji = get_food_emoji(dinner["dish"])
            st.markdown(render_meal_card("dinner", dinner, emoji), unsafe_allow_html=True)

        # 合计栏（CSV 存单价，两人总价 = 单价×2）
        lunch_per = lunch["cost"]
        dinner_per = dinner["cost"]
        total_two = (lunch_per + dinner_per) * 2

        if total_two <= budget_used:
            bar_class = "total-bar in-budget"
            icon = "✅"
            msg = (
                f"午饭 {fmt_price(lunch_per)}×2 + 晚饭 {fmt_price(dinner_per)}×2 "
                f"= {fmt_price(total_two)} / ¥{budget_used} — 在预算内，完美！"
            )
        else:
            bar_class = "total-bar over-budget"
            icon = "⚠️"
            msg = f"合计 {fmt_price(total_two)} / ¥{budget_used} — 超出 ¥{total_two - budget_used}"

        st.markdown(
            f'<div class="{bar_class}">{icon} {msg}</div>',
            unsafe_allow_html=True
        )

    elif st.session_state.locked_budget is not None and st.session_state.current_pick is None:
        st.markdown("---")
        st.warning("😢 当前预算下没有合适的组合，试试调高预算吧～")

    # 历史记录
    if st.session_state.history:
        st.markdown("---")
        with st.expander("📋 抽签记录", expanded=False):
            for idx, record in enumerate(st.session_state.history):
                total_mark = "✅" if record["total"] <= record["budget"] else "⚠️"
                st.markdown(
                    f"""<div class="history-item">
                        <span class="time">🕐 {record["time"]}</span>&nbsp;&nbsp;
                        <strong>#{idx+1}</strong>&nbsp;
                        🌤️ {record["lunch"]}&nbsp;+&nbsp;
                        🌙 {record["dinner"]}&nbsp;&nbsp;
                        {total_mark} ¥{record["total"]} / ¥{record["budget"]}
                    </div>""",
                    unsafe_allow_html=True
                )

# ==================== Tab 2：菜谱管理 ====================
with tab2:
    st.markdown("### 📝 菜谱管理")
    st.markdown("像 Excel 一样编辑，修改后保存或导出～")

    CSV_PATH = Path(__file__).parent / "outside_menu.csv"

    # ---- 上传 CSV 恢复数据 ----
    uploaded_file = st.file_uploader(
        "📥 上传之前导出的 CSV 来恢复菜谱",
        type=["csv"],
        help="如果你之前下载过菜谱 CSV，可以在这里上传恢复"
    )
    if uploaded_file is not None:
        uploaded_df = pd.read_csv(uploaded_file)
        uploaded_df = uploaded_df.dropna(how="all")
        uploaded_df = uploaded_df.dropna(subset=["restaurant", "dish", "cost"])
        uploaded_df.to_csv(CSV_PATH, index=False)
        st.cache_data.clear()
        load_menu.clear()
        st.success(f"✅ 已导入 **{len(uploaded_df)}** 道菜品！")
        st.rerun()

    # ---- 可编辑表格 ----
    # 加载原始数据用于编辑
    raw_df = pd.read_csv(CSV_PATH)
    raw_df = raw_df.dropna(how="all")
    raw_df = raw_df.dropna(subset=["restaurant", "dish", "cost"])
    raw_df["cost"] = raw_df["cost"].astype(float)

    edited_df = st.data_editor(
        raw_df,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "meal": st.column_config.SelectboxColumn(
                "用餐时段",
                options=["午餐/晚餐", "午餐", "晚餐"],
                default="午餐/晚餐",
                width="small",
            ),
            "restaurant": st.column_config.TextColumn(
                "餐厅名",
                width="medium",
            ),
            "dish": st.column_config.TextColumn(
                "菜品名",
                width="medium",
            ),
            "cost": st.column_config.NumberColumn(
                "单价 /人 (¥)",
                min_value=0,
                step=1,
                width="small",
            ),
        },
    )

    col_save, col_download, col_reset = st.columns([1, 1, 1])
    with col_save:
        if st.button("💾 保存到本地", use_container_width=True):
            edited_df.to_csv(CSV_PATH, index=False)
            st.cache_data.clear()
            load_menu.clear()
            st.success("✅ 保存成功！切换回「随机选择」标签即可用")
    with col_download:
        csv_data = edited_df.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            label="📥 导出 CSV",
            data=csv_data,
            file_name="eat_with_you_menu.csv",
            mime="text/csv",
            use_container_width=True,
            help="下载当前菜谱为 CSV 文件，下次可以上传恢复"
        )
    with col_reset:
        if st.button("🔄 撤销修改", use_container_width=True):
            st.rerun()

    st.caption(f"📊 当前共 **{len(raw_df)}** 道菜品")
    st.info(
        "💡 **云部署提示**：在网页上「保存到本地」只对当前会话有效哦。"
        "想永久保留修改，请点击「📥 导出 CSV」下载到电脑，下次打开时上传恢复。"
        "或者直接在 [GitHub](https://github.com/ytu2023/eat_with_you/blob/main/outside_menu.csv) 上编辑 CSV 文件。"
    )

# ============================================================
# 页脚
# ============================================================
st.markdown(
    '<div class="footer">🍽️ 今天和你一起吃什么 · 每天都要好好吃饭 💕</div>',
    unsafe_allow_html=True
)
#2026.07.23 