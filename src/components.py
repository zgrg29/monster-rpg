# -*- coding: utf-8 -*-
"""
src/components.py
UI 组件：横向一排 4 人小队展示，并高亮当前行动角色。
"""

import streamlit as st

def render_enemy_display(enemy):
    """渲染屏幕正中间的敌人立绘与状态区"""
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"<h1 style='text-align: center; font-size: 50px; margin: 0;'>{enemy['avatar']}</h1>", unsafe_allow_html=True)
        st.markdown(f"<h4 style='text-align: center; margin: 0;'>{enemy['name']}</h4>", unsafe_allow_html=True)
    
    hp_percent = max(0.0, min(1.0, enemy["hp"] / enemy["max_hp"]))
    st.markdown(f"**❤️ 敌人生命值**: {enemy['hp']} / {enemy['max_hp']}")
    st.progress(hp_percent)
    st.info(f"🛡️ **护盾**: {enemy['shield']}层 | ⚡ **蓄能**: {enemy['charge']}/{enemy['max_charge']} \n\n 💡 **机制**: {enemy['status_desc']}")
    st.markdown("---")

def render_party_row(party, current_index):
    """
    将己方小队改为横向一排 4 列，轮到行动的角色高亮显示
    """
    st.markdown("#### 🛡️ 己方小队 (行动顺序)")
    cols = st.columns(4)
    role_labels = ["👑 主角", "🤝 伙伴1", "🤝 伙伴2", "🤝 伙伴3"]
    
    for i, member in enumerate(party):
        with cols[i]:
            # 判断是否是当前行动的角色
            is_active = (i == current_index) and (member is not None)
            
            with st.container(border=True):
                if is_active:
                    st.markdown(f"<p style='color: orange; font-weight: bold; font-size: 11px; margin:0;'>▶ 【行动中】</p>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<p style='color: gray; font-size: 11px; margin:0;'>{role_labels[i]}</p>", unsafe_allow_html=True)
                
                if member is not None:
                    st.markdown(f"**{member['name']}**")
                    st.text(f"HP:{member['hp']}")
                    hp_p = max(0.0, min(1.0, member["hp"] / member["max_hp"]))
                    st.progress(hp_p)
                else:
                    st.markdown("<p style='color: gray; text-align: center; font-size: 11px;'>[ 空位 ]</p>", unsafe_allow_html=True)

def render_combat_logs(logs):
    """渲染战报日志"""
    with st.expander("📜 实时战报日志", expanded=False):
        for log in reversed(logs[-8:]):
            st.markdown(f"- {log}")
