# 🍽️ 今天和你一起吃什么

一个基于 Streamlit 的两人用餐随机选择器。根据预算，随机推荐午饭和晚饭，确保总价不超预算。

## 功能

- 💰 滑动选择两人总预算（¥10-100）
- 🎲 一键随机抽取午饭+晚饭组合（总价 ≤ 预算）
- 🔄 不满意？点"再试一次"重新抽取
- 📋 抽签历史记录
- 🎨 温暖浪漫的视觉风格

## 启动方式

```bash
pip install -r requirements.txt
streamlit run eat_with_you.py
```
## 云部署
网址如下：
`https://eatwithyoupy.streamlit.app/`

## 技术栈

- Python 3.11+
- Streamlit
- Pandas

## 如何修改并保存菜单
在`https://github.com/ytu2023/eat_with_you/edit/main/outside_menu.csv`点击修改文件，修改完后保存一下就好了。
