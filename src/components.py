# -*- coding: utf-8 -*-
"""
src/components.py
UI 组件封装：为手机端网页优化的 Streamlit 组件（敌人状态展示、4空格小队网格、战斗日志区）。
"""

import streamlit as st

def render_enemy_display(enemy):
    """
    渲染屏幕正中间的敌人（机制怪）立绘与状态区
    """
    st.markdown("---")
    
    # 模拟手机端居中的视觉卡片
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"<h1 style='text-align: center; font-size: 60px; margin: 0;'>{enemy['avatar']}</h1>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align: center; margin: 0;'>{enemy['name']}</h3>", unsafe_allow_html=True)
    
    # 敌人血量与护盾进度条
    hp_percent = max(0.0, min(1.0, enemy["hp"] / enemy["max_hp"]))
    st.markdown(f"**❤️ 敌人生命值**: {enemy['hp']} / {enemy['max_hp']}")
    st.progress(hp_percent)
    
    # 特殊机制状态标签
    st.info(f"🛡️ **护盾层数**: {enemy['shield']}层 | ⚡ **大招蓄能**: {enemy['charge']}/{enemy['max_charge']} \n\n 💡 **机制提示**: {enemy['status_desc']}")
    st.markdown("---")

def render_party_grid(party):
    """
    渲染屏幕下方的 4 个格子小队网格（1主 + 最多3伙伴）
    """
    st.markdown("#### 🛡️ 己方小队 (4宫格)")
    
    # 使用 2x2 网格完美适配手机端屏幕
    row1 = st.columns(2)
    row2 = st.columns(2)
    grid_cols = [row1[0], row1[1], row2[0], row2[1]]
    
    role_titles = ["👑 主角 (Leader)", "🤝 伙伴槽 1", "🤝 伙伴槽 2", "🤝 伙伴槽 3"]
    
    for i, member in enumerate(party):
        with grid_cols[i]:
            with st.container(border=True):
                st.markdown(f"**{role_titles[i]}**")
                if member is not None:
                    hp_p = member["hp"] / member["max_hp"]
                    st.markdown(f"**{member['name']}**")
                    st.text(f"HP: {member['hp']}/{member['max_hp']}")
                    st.progress(hp_p)
                else:
                    st.markdown("<p style='color: gray; text-align: center;'>[ 空位 / 待收复 ]</p>", unsafe_allow_html=True)

def render_combat_logs(logs):
    """
    渲染战斗战报滚动区
    """
    with st.expander("📜 实时战报日志 (Combat Log)", expanded=True):
        # 倒序展示最新的日志在最上面
        for log in reversed(logs[-8:]):
            st.markdown(f"- {log}")
