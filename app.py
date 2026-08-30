# -*- coding: utf-8 -*-
import streamlit as st
from src.game_state import init_game_state, reset_game
from src.combat_engine import process_player_action, process_enemy_turn
from src.components import render_enemy_display, render_party_row, render_combat_logs

st.set_page_config(
    page_title="机甲少女战记 - 策略 RPG",
    page_icon="⚔️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

init_game_state()

player = st.session_state.player
enemy = st.session_state.current_enemy
party = st.session_state.party
logs = st.session_state.combat_logs

# ==================== 单屏战斗画面 ====================

# 固定高度容器
st.markdown("""
<style>
.battle-wrapper {
    height: 92vh; 
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
.compact-text {
    font-size: 0.9rem;
    line-height: 1.2rem;
}
</style>
<div class="battle-wrapper">
""", unsafe_allow_html=True)

# 1. 敌人区（压缩版）
with st.container():
    st.markdown(f"""
        <div class="compact-text">
        <b>🟥 {enemy['name']}</b><br>
        ❤️ HP: {enemy['hp']} / {enemy['max_hp']}<br>
        🛡 护盾: {enemy['shield']} | ⚡ 蓄能: {enemy['charge']}/4<br>
        <i>机制：{enemy['mechanic']}</i>
        </div>
    """, unsafe_allow_html=True)

# 2. 己方队伍区（压缩版）
with st.container():
    render_party_row(party, st.session_state.current_actor_index)

# 3. 指令区（压缩按钮）
current_idx = st.session_state.current_actor_index
active_actor = party[current_idx]

st.markdown(
    f"#### 🎮 指令（{active_actor['name']}）",
    unsafe_allow_html=True
)

phys = player["proficiencies"]["physical"]
magic = player["proficiencies"]["magic"]
defn = player["proficiencies"]["defense"]
heal = player["proficiencies"]["heal"]

row1 = st.columns(2)
row2 = st.columns(2)

def advance_turn():
    next_idx = st.session_state.current_actor_index + 1
    found = False
    while next_idx < 4:
        if party[next_idx] is not None:
            st.session_state.current_actor_index = next_idx
            found = True
            break
        next_idx += 1
    if not found:
        st.session_state.current_actor_index = 0
        logs.extend(process_enemy_turn(party, enemy))

with row1[0]:
    if st.button(f"⚔️ 物理\n{int(phys['level']*100)}%", use_container_width=True):
        logs.extend(process_player_action(active_actor, enemy, "physical"))
        advance_turn()
        st.rerun()

with row1[1]:
    if st.button(f"🔮 魔法\n{int(magic['level']*100)}%", use_container_width=True):
        logs.extend(process_player_action(active_actor, enemy, "magic"))
        advance_turn()
        st.rerun()

with row2[0]:
    if st.button(f"🛡 防御\n{int(defn['level']*100)}%", use_container_width=True):
        logs.extend(process_player_action(active_actor, enemy, "defense"))
        advance_turn()
        st.rerun()

with row2[1]:
    if st.button(f"✨ 回复\n{int(heal['level']*100)}%", use_container_width=True):
        logs.extend(process_player_action(active_actor, enemy, "heal"))
        advance_turn()
        st.rerun()

# 战报日志折叠，不占空间
with st.expander("📜 战报日志（点击展开）"):
    render_combat_logs(logs)

st.markdown("</div>", unsafe_allow_html=True)
