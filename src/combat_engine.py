# -*- coding: utf-8 -*-
"""
src/combat_engine.py
战斗逻辑引擎：处理熟练度成长、伤害/命中率计算、敌人特殊机制（护盾与蓄能）及战斗结算。
"""

import random

def calculate_proficiency_effect(proficiency_data):
    """
    根据当前熟练度计算实际效果加成
    - 熟练度等级 (level): 0.0 到 1.0 (代表 0% 到 100%)
    - 初始（0%）：伤害/效果 = 50%，命中率 = 50%
    - 满级（100%）：伤害/效果 = 100%，命中率 = 100%
    - 突破 100% 后有概率触发暴击/觉醒
    """
    level = proficiency_data["level"]
    base_power = proficiency_data["base_power"]
    
    # 基础命中率：50% 线性提升至 100%
    hit_rate = 0.5 + (level * 0.5)
    
    # 基础威力：50% 线性提升至 100%
    power_multiplier = 0.5 + (level * 0.5)
    
    # 判定是否命中
    is_hit = random.random() <= hit_rate
    if not is_hit:
        return 0, False, False, "未命中"
    
    # 计算基础伤害/效果
    final_value = base_power * power_multiplier
    
    # 突破判定（如果 level >= 1.0，有 30% 概率触发超频觉醒暴击 150%）
    is_crit = False
    if level >= 1.0 and random.random() < 0.3:
        final_value *= 1.5
        is_crit = True
        
    return int(final_value), True, is_crit, "成功"

def update_proficiency(proficiency_data):
    """
    使用后提升熟练度
    每次使用增加 0.1 (10%)，上限可以超过 1.0 开启超频
    """
    proficiency_data["uses"] += 1
    # 熟练度上限设为 1.5 (150%)，每次提升 0.1
    if proficiency_data["level"] < 1.5:
        proficiency_data["level"] = round(min(1.5, proficiency_data["level"] + 0.1), 2)

def process_player_action(player, enemy, action_type):
    """
    处理玩家的回合行动
    action_type: 'weapon' (武器), 'skill' (战技), 'magic' (魔法)
    """
    logs = []
    prof = player["proficiencies"][action_type]
    
    # 计算本次动作效果
    value, is_hit, is_crit, msg = calculate_proficiency_effect(prof)
    update_proficiency(prof)
    
    if not is_hit:
        logs.append(f"你使用了【{prof['name']}】，但被敌人闪避了！(熟练度: int({prof['level']*100}%))")
        return logs

    # 根据不同动作类型处理对敌人的效果
    if action_type in ["weapon", "skill"]:
        # 物理攻击结算（受敌人护盾机制影响）
        if action_type == "weapon" and enemy["shield"] > 0:
            enemy["shield"] -= 1
            logs.append(f"你使用了【{prof['name']}】！触发了物理攻击。敌人护盾生效，免疫伤害，但护盾剩余层数：{enemy['shield']}")
        else:
            # 破盾后或战技直接造成伤害
            damage = value
            if is_crit:
                damage = int(damage * 1.5)
                logs.append(f"✨ **【超频觉醒暴击】**！你使用了【{prof['name']}】，造成了高额伤害 {damage} 点！")
            else:
                logs.append(f"你使用了【{prof['name']}】，造成了 {damage} 点伤害。")
            enemy["hp"] = max(0, enemy["hp"] - damage)
            
    elif action_type == "magic":
        # 魔法攻击可以无视护盾直接造成伤害，或附带特殊效果
        damage = value
        if is_crit:
            damage = int(damage * 1.5)
            logs.append(f"✨ **【魔法回响暴击】**！【{prof['name']}】涌现强光，对敌人造成 {damage} 点魔法伤害并削减其蓄能！")
            if enemy["charge"] > 0:
                enemy["charge"] -= 1
        else:
            logs.append(f"你释放了【{prof['name']}】，对敌人造成 {damage} 点魔法伤害（无视护盾）。")
        enemy["hp"] = max(0, enemy["hp"] - damage)

    return logs

def process_enemy_turn(player, enemy):
    """
    处理敌人的回合反击机制
    """
    logs = []
    if enemy["hp"] <= 0:
        return logs

    # 敌人蓄能机制推进
    enemy["charge"] += 1
    
    if enemy["charge"] >= enemy["max_charge"]:
        # 释放大招
        boss_damage = 60
        player["hp"] = max(0, player["hp"] - boss_damage)
        enemy["charge"] = 0
        logs.append(f"⚠️ **【{enemy['name']}】释放了全屏毁灭打击！** 对你造成了重创 {boss_damage} 点伤害！")
    else:
        # 普通攻击
        boss_damage = 20
        player["hp"] = max(0, player["hp"] - boss_damage)
        logs.append(f"【{enemy['name']}】发动反击，对你造成了 {boss_damage} 点伤害。（蓄能：{enemy['charge']}/{enemy['max_charge']}）")
        
    return logs
