# -*- coding: utf-8 -*-
"""
src/game_state.py
全局状态管理：使用 Streamlit 的 session_state 初始化和维护游戏核心数据。
"""

import streamlit as st
from src.data import INITIAL_PLAYER, FIRST_BOSS

def init_game_state():
    """初始化全局游戏状态（如果不存在的话）"""
    
    # 游戏流程阶段: "battle" (战斗中), "victory" (胜利/收复结算), "defeat" (失败)
    if "game_phase" not in st.session_state:
        st.session_state.game_phase = "battle"

    # 主角状态
    if "player" not in st.session_state:
        st.session_state.player = INITIAL_PLAYER.copy()

    # 4空格小队系统：最多 4 个格子 [主角, 伙伴1, 伙伴2, 伙伴3]
    # 格子为 None 代表空位
    if "party" not in st.session_state:
        st.session_state.party = [
            st.session_state.player,  # 0号位固定为主角
            None,                     # 伙伴槽 1
            None,                     # 伙伴槽 2
            None                      # 伙伴槽 3
        ]

    # 当前敌人状态（深拷贝以防直接修改原始数据）
    if "current_enemy" not in st.session_state:
        st.session_state.current_enemy = FIRST_BOSS.copy()

    # 战斗日志（记录每回合的行动结果）
    if "combat_logs" not in st.session_state:
        st.session_state.combat_logs = [
            "【战斗开始】遭遇了机制怪：机甲少女·阿尔法！",
            "提示：敌人带有【绝对防御】护盾，普通物理攻击可能无法奏效，请合理选择战技或魔法！"
        ]

def reset_game():
    """重置游戏状态"""
    st.session_state.game_phase = "battle"
    st.session_state.player = INITIAL_PLAYER.copy()
    st.session_state.party = [st.session_state.player, None, None, None]
    st.session_state.current_enemy = FIRST_BOSS.copy()
    st.session_state.combat_logs = ["【游戏重置】新的一轮挑战开始了！"]
