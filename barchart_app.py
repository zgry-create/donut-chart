import streamlit as st
import matplotlib.pyplot as plt
import io
import numpy as np

st.set_page_config(page_title="水平条形图生成器", layout="centered")
st.title("水平条形图生成器")
st.markdown("可选择输入百分比或原始数值（自动计算百分比），生成无文字说明的横版条形图。")

# 初始化 session_state
if "mode" not in st.session_state:
    st.session_state.mode = "百分比模式"
if "data" not in st.session_state:
    st.session_state.data = [("0-9", 1270), ("10-19", 1916), ("20-29", 1926), ("30-39", 2057), ("40-49", 2529)]

# 模式选择
mode = st.radio("输入模式", ["百分比模式", "原始数值模式"], horizontal=True, index=0 if st.session_state.mode == "百分比模式" else 1)
st.session_state.mode = mode

# 数据编辑区域
st.subheader("数据编辑")
col1, col2 = st.columns([3, 1])
with col1:
    st.write("类别")
with col2:
    st.write("数值")

for i, (label, val) in enumerate(st.session_state.data):
    cols = st.columns([3, 1, 0.5])
    with cols[0]:
        new_label = st.text_input("类别", value=label, key=f"label_{i}", label_visibility="collapsed")
    with cols[1]:
        new_val = st.number_input("数值", value=float(val), step=1.0, key=f"val_{i}", label_visibility="collapsed")
    with cols[2]:
        if st.button("删除", key=f"del_{i}"):
            st.session_state.data.pop(i)
            st.rerun()
    # 更新数据
    st.session_state.data[i] = (new_label, new_val)

# 添加新项
if st.button("添加一项"):
    st.session_state.data.append(("新类别", 0.0))
    st.rerun()

# 图形设置
st.subheader("图形设置")
fig_width = st.slider("图形宽度（英寸）", 6, 12, 8)
fig_height = st.slider("图形高度（英寸）", 4, 10, 6)
bar_color = st.color_picker("条形颜色", "#4A90E2")
show_percent_labels = st.checkbox("显示百分比标签", value=True)

# 生成按钮
if st.button("生成条形图"):
    if len(st.session_state.data) == 0:
        st.error("至少需要一项数据")
    else:
        # 提取类别和数值
        labels = [item[0] for item in st.session_state.data]
        values = [item[1] for item in st.session_state.data]

        # 根据模式计算百分比
        if mode == "百分比模式":
            # 直接使用输入值作为百分比（可能不为100，但保留原样）
            percentages = values
            # 可选：提示总和不为100，但不影响绘制
            total = sum(values)
            if abs(total - 100) > 0.1:
                st.warning(f"百分比总和为 {total:.1f}%，不是100%")
        else:
            # 原始数值模式：自动计算百分比
            total = sum(values)
            if total == 0:
                st.error("总和为0，无法计算百分比")
                st.stop()
            percentages = [v / total * 100 for v in values]

        # 绘制水平条形图
        fig, ax = plt.subplots(figsize=(fig_width, fig_height))
        bars = ax.barh(labels, percentages, color=bar_color, edgecolor='white', linewidth=0.5)

        # 显示百分比标签
        if show_percent_labels:
            for bar in bars:
                width = bar.get_width()
                ax.text(width + 0.3, bar.get_y() + bar.get_height()/2,
                        f'{width:.1f}%', va='center', fontsize=9, color='black')

        # 去除所有文字说明（标题、轴标签、刻度标签可选保留）
        ax.set_title("")          # 无标题
        ax.set_xlabel("")         # 无x轴标签
        ax.set_ylabel("")         # 无y轴标签
        # 可选：去除刻度标签（如果需要完全无文字，取消下面注释）
        # ax.set_xticklabels([])
        # ax.set_yticklabels([])

        # 去除边框（可选）
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        plt.tight_layout()

        # 保存到内存并显示
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=300, bbox_inches='tight')
        buf.seek(0)
        st.image(buf, caption="生成的条形图", use_column_width=True)
        st.download_button("下载 PNG 图片", data=buf, file_name="barchart.png", mime="image/png")
        plt.close(fig)