# -*- coding: utf-8 -*-
"""
app.py
Streamlit 手机端策略 RPG 主入口（4 基础指令：物理、魔法、防御、回复）
"""

import streamlit as st
from src.game_state import init_game_state, reset_game
from src.combat_engine import process_player_action, process_enemy_turn
from src.components import render_enemy_display, render_party_row, render_combat_logs

# 1. 页面基本配置
st.set_page_config(
    page_title="机甲少女战记 - 策略 RPG",
    page_icon="⚔️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. 初始化全局状态
init_game_state()

player = st.session_state.player
enemy = st.session_state.current_enemy
party = st.session_state.party
logs = st.session_state.combat_logs

# 3. 页面标题
st.markdown("<h2 style='text-align: center;'>⚔️ 机制怪策略战记</h2>", unsafe_allow_html=True)

# 4. 检查胜负状态
if enemy["hp"] <= 0:
    st.success("🎉 **战斗胜利！** 你成功击败了机甲少女·阿尔法！")
    st.balloons()
    if st.button("🔄 重新开始新一轮挑战", use_container_width=True):
        reset_game()
        st.rerun()
    st.stop()

if player["hp"] <= 0:
    st.error("💀 **战斗失败...** 主角倒下了，世界陷入黑暗。")
    if st.button("🔄 恢复状态，重整旗鼓", use_container_width=True):
        reset_game()
        st.rerun()
    st.stop()

# ==================== 📌 单屏战斗画面布局 ====================

# 固定高度容器，让敌人区 + 队伍区 + 指令区全部在一个屏幕内
st.markdown("""
    <style>
        .battle-wrapper {
            height: 88vh;                 /* 固定在一个屏幕高度内 */
            display: flex;
            flex-direction: column;
            justify-content: space-between;  /* 上中下自动分布 */
        }
    </style>
    <div class="battle-wrapper">
""", unsafe_allow_html=True)

# 1. 敌人区（顶部）
enemy_area = st.container()
with enemy_area:
    render_enemy_display(enemy)

st.markdown("<hr>", unsafe_allow_html=True)

# 2. 己方队伍区（中间）
team_area = st.container()
with team_area:
    render_party_row(party, st.session_state.current_actor_index)

st.markdown("<hr>", unsafe_allow_html=True)

# 3. 指令区（底部）
current_idx = st.session_state.current_actor_index
active_actor = party[current_idx]

st.markdown(
    f"#### 🎮 战术指令行动区 (当前行动：<span style='color:orange;'>{active_actor['name']}</span>)",
    unsafe_allow_html=True
)

# 熟练度
phys_prof = player["proficiencies"]["physical"]
magic_prof = player["proficiencies"]["magic"]
def_prof = player["proficiencies"]["defense"]
heal_prof = player["proficiencies"]["heal"]

# 按钮布局：2x2 网格
row1_cols = st.columns(2)
row2_cols = st.columns(2)

def advance_turn():
    """推进到下一个角色或触发敌人回合"""
    next_idx = st.session_state.current_actor_index + 1
    found_next = False
    
    while next_idx < 4:
        if party[next_idx] is not None:
            st.session_state.current_actor_index = next_idx
            found_next = True
            break
        next_idx += 1
        
    if not found_next:
        st.session_state.current_actor_index = 0
        if enemy["hp"] > 0:
            logs.extend(process_enemy_turn(party, enemy))

with row1_cols[0]:
    if st.button(f"⚔️ 物理攻击\n({int(phys_prof['level']*100)}%)", use_container_width=True):
        logs.extend(process_player_action(active_actor, enemy, "physical"))
        advance_turn()
        st.rerun()

with row1_cols[1]:
    if st.button(f"🔮 魔法攻击\n({int(magic_prof['level']*100)}%)", use_container_width=True):
        logs.extend(process_player_action(active_actor, enemy, "magic"))
        advance_turn()
        st.rerun()

with row2_cols[0]:
    if st.button(f"🛡️ 防御\n({int(def_prof['level']*100)}%)", use_container_width=True):
        logs.extend(process_player_action(active_actor, enemy, "defense"))
        advance_turn()
        st.rerun()

with row2_cols[1]:
    if st.button(f"✨ 回复\n({int(heal_prof['level']*100)}%)", use_container_width=True):
        logs.extend(process_player_action(active_actor, enemy, "heal"))
        advance_turn()
        st.rerun()

# 战报日志沉底（自动缩放，不会挤出去）
render_combat_logs(logs)

st.markdown("</div>", unsafe_allow_html=True)

# 侧边栏：查看属性与熟练度
with st.sidebar:
    st.markdown("### 📊 主角成长面板")
    st.text(f"当前生命: {player['hp']} / {player['max_hp']}")
    st.markdown("---")
    st.markdown("#### 📈 熟练度详情")
    for key, p_data in player["proficiencies"].items():
        st.markdown(f"**{p_data['name']}**")
        st.text(f"使用次数: {p_data['uses']} | 熟练度: {int(p_data['level']*100)}%")
        st.progress(min(1.0, p_data['level']))
