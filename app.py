import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="圆环图生成器", layout="centered")
st.title("圆环图生成器")
st.markdown("输入各部分的百分比（总和可为任意值，程序自动归一化）")

# 数据输入：动态添加
if "data" not in st.session_state:
    st.session_state.data = [41.0, 48.5]  # 初始值

# 显示现有数据
cols = st.columns([3, 1])
for i, val in enumerate(st.session_state.data):
    with st.container():
        col1, col2 = st.columns([3, 1])
        with col1:
            new_val = st.number_input(f"项 {i+1}", value=val, step=0.1, format="%.1f", key=f"input_{i}")
            st.session_state.data[i] = new_val
        with col2:
            if st.button("删除", key=f"del_{i}"):
                st.session_state.data.pop(i)
                st.rerun()

# 添加新项
if st.button("添加一项"):
    st.session_state.data.append(0.0)
    st.rerun()

# 圆环宽度控制
inner_radius = st.slider("中心圆半径（越小环越宽）", 0.1, 0.9, 0.40, step=0.01)

# 颜色方案（可自定义）
color_palette = [
    '#FFB6C1', '#87CEEB', '#98FB98', '#FFD700',
    '#D3D3D3', '#FFA07A', '#9370DB', '#F4A460'
]

if st.button("生成圆环图"):
    data = [v for v in st.session_state.data if v > 0]
    if not data:
        st.error("至少需要一项正数")
    else:
        # 归一化
        total = sum(data)
        normalized = [v / total * 100 for v in data]
        colors = color_palette * (len(normalized) // len(color_palette) + 1)
        colors = colors[:len(normalized)]

        fig, ax = plt.subplots(figsize=(8, 6))
        wedges = ax.pie(
            normalized,
            colors=colors,
            startangle=90,
            wedgeprops={'edgecolor': 'white', 'linewidth': 2}
        )[0]
        centre_circle = plt.Circle((0, 0), inner_radius, fc='white', linewidth=2, edgecolor='white')
        ax.add_artist(centre_circle)
        ax.axis('equal')
        plt.tight_layout()

        # 保存图片并提供下载
        import io
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=300, bbox_inches='tight')
        buf.seek(0)
        st.image(buf, caption="生成的圆环图", use_column_width=True)
        st.download_button("下载 PNG 图片", data=buf, file_name="donut_chart.png", mime="image/png")
        plt.close(fig)