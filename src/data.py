# -*- coding: utf-8 -*-
"""
src/data.py
游戏静态数据配置：包含主角初始属性、熟练度结构、敌人（机制怪）数据及装备词缀。
"""

# 主角初始配置
INITIAL_PLAYER = {
    "name": "流浪者",
    "hp": 150,
    "max_hp": 150,
    "mp": 100,
    "max_mp": 100,
    # 熟练度系统：uses (使用次数), level (熟练度百分比 0~100+)
    "proficiencies": {
        "weapon": {
            "name": "重剑斩击", 
            "type": "weapon",
            "uses": 0, 
            "level": 0.0, # 0.0 代表 0%，1.0 代表 100%
            "base_power": 40
        },
        "skill": {
            "name": "战术架势", 
            "type": "skill",
            "uses": 0, 
            "level": 0.0,
            "base_power": 25
        },
        "magic": {
            "name": "微光治愈", 
            "type": "magic",
            "uses": 0, 
            "level": 0.0,
            "base_power": 30
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
    "shield": 3,          # 特殊机制：3层物理免伤盾（必须通过魔法或破盾技能消耗）
    "charge": 0,          # 大招蓄能进度（满 4 回合释放全屏毁灭打击）
    "max_charge": 4,
    "status_desc": "【绝对防御】免疫前3次物理攻击",
    "avatar": "🤖",       # 手机端临时用 Emoji 代替立绘，后续可换图片路径
    "drop_reward": "阿尔法的核心零件"
}

# 基础装备/词缀库
EQUIPMENT_POOL = [
    {
        "id": "eq_01",
        "name": "吸血鬼指环",
        "slot": "accessory",
        "description": "每次造成伤害时，将 20% 转化为自身生命，但无法接受外部治疗。",
        "trait": "vampire"
    },
    {
        "id": "eq_02",
        "name": "重装力场组件",
        "slot": "armor",
        "description": "免疫暴击伤害，但行动速度/熟练度获取效率降低 20%。",
        "trait": "heavy_shield"
    }
]
