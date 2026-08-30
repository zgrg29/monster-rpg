# -*- coding: utf-8 -*-
"""
src/combat_engine.py
战斗逻辑引擎：处理 4 种行动指令的熟练度与结算。
"""

import random

def calculate_proficiency_effect(proficiency_data):
    """计算熟练度带来的效果与暴击判定"""
    level = proficiency_data["level"]
    base_power = proficiency_data["base_power"]
    
    hit_rate = 0.5 + (level * 0.5)
    power_multiplier = 0.5 + (level * 0.5)
    
    is_hit = random.random() <= hit_rate
    if not is_hit:
        return 0, False, False, "未命中"
    
    final_value = base_power * power_multiplier
    
    is_crit = False
    if level >= 1.0 and random.random() < 0.3:
        final_value *= 1.5
        is_crit = True
        
    return int(final_value), True, is_crit, "成功"

def update_proficiency(proficiency_data):
    """提升熟练度"""
    proficiency_data["uses"] += 1
    if proficiency_data["level"] < 1.5:
        proficiency_data["level"] = round(min(1.5, proficiency_data["level"] + 0.1), 2)

def process_player_action(actor, enemy, action_type):
    """
    处理 4 种行动:
    - physical: 物理攻击
    - magic: 魔法攻击
    - defense: 防御状态
    - heal: 回复生命
    """
    logs = []
    prof = actor["proficiencies"][action_type]
    value, is_hit, is_crit, msg = calculate_proficiency_effect(prof)
    update_proficiency(prof)
    
    # 记录是否处于防御状态（可存在 actor 临时属性中）
    actor.setdefault("is_defending", False)
    actor["is_defending"] = False  # 先重置，除非本回合选了防御

    if action_type == "physical":
        if not is_hit:
            logs.append(f"【{actor['name']}】使用了【{prof['name']}】，但被敌人闪避了！")
            return logs
            
        if enemy["shield"] > 0:
            enemy["shield"] -= 1
            logs.append(f"【{actor['name']}】使用了【{prof['name']}】！触发物理攻击，被敌人护盾抵挡，护盾剩余：{enemy['shield']}")
        else:
            damage = int(value * 1.5) if is_crit else value
            crit_str = "✨ **【暴击】**" if is_crit else ""
            logs.append(f"【{actor['name']}】使用【{prof['name']}】{crit_str}，对敌人造成了 {damage} 点物理伤害！")
            enemy["hp"] = max(0, enemy["hp"] - damage)

    elif action_type == "magic":
        if not is_hit:
            logs.append(f"【{actor['name']}】释放【{prof['name']}】，法术失控未命中！")
            return logs
            
        damage = int(value * 1.5) if is_crit else value
        crit_str = "✨ **【魔法回响】**" if is_crit else ""
        logs.append(f"【{actor['name']}】释放【{prof['name']}】{crit_str}，无视护盾对敌人造成 {damage} 点法术伤害！")
        enemy["hp"] = max(0, enemy["hp"] - damage)

    elif action_type == "defense":
        actor["is_defending"] = True
        shield_buff = value
        logs.append(f"🛡️ 【{actor['name']}】采取了【防御姿态】，严阵以待，本回合受到的伤害大幅降低！")

    elif action_type == "heal":
        heal_val = int(value * 1.5) if is_crit else value
        actor["hp"] = min(actor["max_hp"], actor["hp"] + heal_val)
        crit_str = "✨ **【强效治愈】**" if is_crit else ""
        logs.append(f"✨ 【{actor['name']}】使用了【{prof['name']}】{crit_str}，为自己恢复了 {heal_val} 点生命值！")

    return logs

def process_enemy_turn(party, enemy):
    """敌人的反击回合（考虑队员的防御状态进行减伤）"""
    logs = []
    if enemy["hp"] <= 0:
        return logs

    enemy["charge"] += 1
    
    if enemy["charge"] >= enemy["max_charge"]:
        base_dmg = 60
        enemy["charge"] = 0
        logs.append(f"⚠️ **【{enemy['name']}】释放了全屏毁灭打击！**")
        for member in party:
            if member is not None and member["hp"] > 0:
                actual_dmg = int(base_dmg / 2) if member.get("is_defending") else base_dmg
                member["hp"] = max(0, member["hp"] - actual_dmg)
                def_str = "（防御减伤生效）" if member.get("is_defending") else ""
                logs.append(f"- 【{member['name']}】受到 {actual_dmg} 点伤害 {def_str}")
    else:
        base_dmg = 20
        logs.append(f"【{enemy['name']}】发动反击！（蓄能：{enemy['charge']}/{enemy['max_charge']}）")
        for member in party:
            if member is not None and member["hp"] > 0:
                actual_dmg = int(base_dmg / 2) if member.get("is_defending") else base_dmg
                member["hp"] = max(0, member["hp"] - actual_dmg)
                def_str = "（防御减伤）" if member.get("is_defending") else ""
                logs.append(f"- 【{member['name']}】受到 {actual_dmg} 点伤害 {def_str}")
                
    return logs
