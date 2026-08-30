# -*- coding: utf-8 -*-
"""
src/data.py
游戏静态数据配置：包含主角初始属性、熟练度结构、敌人数据及装备词缀。
"""

# 主角初始配置
INITIAL_PLAYER = {
    "name": "流浪者",
    "hp": 150,
    "max_hp": 150,
    "mp": 100,
    "max_mp": 100,
    # 4 种基础指令的熟练度体系
    "proficiencies": {
        "physical": {
            "name": "物理斩击", 
            "type": "physical",
            "uses": 0, 
            "level": 0.0, 
            "base_power": 45
        },
        "magic": {
            "name": "元素法球", 
            "type": "magic",
            "uses": 0, 
            "level": 0.0,
            "base_power": 40
        },
        "defense": {
            "name": "战术防御", 
            "type": "defense",
            "uses": 0, 
            "level": 0.0,
            "base_power": 20  # 代表减伤/护盾值
        },
        "heal": {
            "name": "急救回复", 
            "type": "heal",
            "uses": 0, 
            "level": 0.0,
            "base_power": 35  # 代表回复血量值
        },
    },
    "equipment": {
        "weapon": {"name": "铁制长剑", "effect": "无特殊效果"},
        "armor": {"name": "布甲", "effect": "无特殊效果"}
    }
}

# 第一个机制怪：机械人偶少女
FIRST_BOSS = {
    "id": "boss_01",
    "name": "机甲少女·阿尔法",
    "hp": 300,
    "max_hp": 300,
    "shield": 3,          # 物理免伤护盾（需通过魔法破除）
    "charge": 0,          # 蓄能
    "max_charge": 4,
    "status_desc": "【绝对防御】免疫物理攻击，需用魔法或持续消耗",
    "avatar": "🤖",
    "drop_reward": "阿尔法的核心零件"
}

# 装备池
EQUIPMENT_POOL = [
    {
        "id": "eq_01",
        "name": "吸血鬼指环",
        "slot": "accessory",
        "description": "每次造成伤害时，将 20% 转化为自身生命。",
        "trait": "vampire"
    }
]
