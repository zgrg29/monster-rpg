# -*- coding: utf-8 -*-
"""
app.py
Streamlit 手机端策略 RPG 主入口（横向小队 + 轮流行动制）
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

# ==================== 手机端黄金视口布局 ====================

# 1. 屏幕正中间 —— 敌人立绘与机制状态
render_enemy_display(enemy)

# 2. 横向一排 4 人小队（高亮当前行动者）
render_party_row(party, st.session_state.current_actor_index)

st.markdown("---")

# 获取当前正在行动的角色
current_idx = st.session_state.current_actor_index
active_actor = party[current_idx]

# 如果当前槽位是空的（比如未来伙伴槽还没招募），自动往后切或触发敌人回合
if active_actor is None:
    # 寻找下一个有效角色或触发敌方回合
    # 简化逻辑：直接推进到下一个或敌人
    pass

st.markdown(f"#### 🎮 战术指令行动区 (当前行动：<span style='color:orange;'>{active_actor['name'] if active_actor else '无'}</span>)", unsafe_allow_html=True)

# 获取熟练度用于按钮展示
weapon_prof = player["proficiencies"]["weapon"]
skill_prof = player["proficiencies"]["skill"]
magic_prof = player["proficiencies"]["magic"]

# 3. 触控操作区
col_a, col_b, col_c = st.columns(3)

def advance_turn():
    """推进回合的通用函数"""
    # 寻找下一个有效队员
    next_idx = st.session_state.current_actor_index + 1
    found_next = False
    
    while next_idx < 4:
        if party[next_idx] is not None:
            st.session_state.current_actor_index = next_idx
            found_next = True
            break
        next_idx += 1
        
    # 如果后面没有队员了，说明小队全部行动完毕，轮到敌人反击！
    if not found_next:
        st.session_state.current_actor_index = 0 # 重置回主角
        if enemy["hp"] > 0:
            enemy_logs = process_enemy_turn(player, enemy)
            logs.extend(enemy_logs)

with col_a:
    btn_text_w = f"⚔️ 武器\n({int(weapon_prof['level']*100)}%)"
    if st.button(btn_text_w, use_container_width=True):
        action_logs = process_player_action(active_actor, enemy, "weapon")
        logs.extend(action_logs)
        advance_turn()
        st.rerun()

with col_b:
    btn_text_s = f"🛡️ 架势\n({int(skill_prof['level']*100)}%)"
    if st.button(btn_text_s, use_container_width=True):
        action_logs = process_player_action(active_actor, enemy, "skill")
        logs.extend(action_logs)
        advance_turn()
        st.rerun()

with col_c:
    btn_text_m = f"✨ 治愈\n({int(magic_prof['level']*100)}%)"
    if st.button(btn_text_m, use_container_width=True):
        action_logs = process_player_action(active_actor, enemy, "magic")
        logs.extend(action_logs)
        advance_turn()
        st.rerun()

# 4. 战报日志沉底
render_combat_logs(logs)

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
