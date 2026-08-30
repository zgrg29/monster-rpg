# -*- coding: utf-8 -*-
"""
src/game_state.py
全局状态管理：包含 4 人小队、当前行动角色指针及敌人状态。
"""

import streamlit as st
from src.data import INITIAL_PLAYER, FIRST_BOSS

def init_game_state():
    """初始化全局游戏状态"""
    if "game_phase" not in st.session_state:
        st.session_state.game_phase = "battle"

    if "player" not in st.session_state:
        st.session_state.player = INITIAL_PLAYER.copy()

    # 4空格小队系统
    if "party" not in st.session_state:
        st.session_state.party = [
            st.session_state.player,  # 0号位：主角
            None,                     # 1号位：伙伴槽 1
            None,                     # 2号位：伙伴槽 2
            None                      # 3号位：伙伴槽 3
        ]

    # 当前轮到小队中的第几个角色行动 (0 到 3)
    if "current_actor_index" not in st.session_state:
        st.session_state.current_actor_index = 0

    if "current_enemy" not in st.session_state:
        st.session_state.current_enemy = FIRST_BOSS.copy()

    if "combat_logs" not in st.session_state:
        st.session_state.combat_logs = [
            "【战斗开始】遭遇了机制怪：机甲少女·阿尔法！",
            "提示：采用轮流行动制，轮到谁操作即可使用对应技能。"
        ]

def reset_game():
    """重置游戏状态"""
    st.session_state.game_phase = "battle"
    st.session_state.player = INITIAL_PLAYER.copy()
    st.session_state.party = [st.session_state.player, None, None, None]
    st.session_state.current_actor_index = 0
    st.session_state.current_enemy = FIRST_BOSS.copy()
    st.session_state.combat_logs = ["【游戏重置】新的一轮挑战开始了！"]
