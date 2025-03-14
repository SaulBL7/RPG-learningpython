import random
import copy
from .levelup import *
from .buff import *

dice = []
for i in range(1, 100):
    dice.append(i)


class Monster:
    def __init__(self, player, difficulty):
        match difficulty:
            case "1" | "Easy":
                self.level = player.level
            case "2" | "Medium":
                self.level = player.level + 1
            case "3" | "Hard":
                self.level = player.level + random.randint(2, 3)
            case "4" | "Boss":
                self.level = player.level + 5

        self.name = f"Monster {self.level}"
        if difficulty in ['4','Boss']:
            self.damage = 6 * self.level
            self.hp = self.hp_max = 140 * self.level
            self.crit = min(50, 10 + round(self.level))
            self.exp = 120 * self.level
            self.gold = 100 * self.level
            self.pdef = 20
            self.mdef = 40
            self.status = 'boss'
        else:
            self.damage = 4 * self.level
            self.hp = self.hp_max = 40 * self.level
            self.crit = min(50, 10 + round(self.level / 2))
            self.exp = 20 * self.level
            self.gold = 30 * self.level
            self.pdef = 0
            self.mdef = 0
            self.status = 'common'


def start_battle(player, difficulty):
    monster = Monster(player, difficulty)
    fight(player, monster)


def fight(player, monster):
    print(f'Monster level {monster.level} encountered')
    while True:
        player.action = False
        available_choices = {"1": "Attack", "2": "Magic", "3": "Status", "4": "Flee"}
        print("-" * 30)
        print(
            f'{player.name} -> HP: {player.hp}/{player.hp_max} | {player.resource.upper()}: {player.mana}/{player.mana_max}')
        print(f'MONSTER -> HP: {monster.hp}/{monster.hp_max} | Damage: {monster.damage}')
        print("-" * 30)
        for num,text in available_choices.items():
            print(f"{num}-{text}", end=' | ')
        choice = input("Choose an action: ").capitalize()

        if choice in available_choices or choice in available_choices.values():
            choice = available_choices.get(choice, choice)
            match choice:
                case '1' | 'Attack':
                    attack(player, monster)
                    player.action = True
                case '2' | 'Magic':
                    use_magic(player, monster)
                case '3' | 'Status':
                    player.status_battle()
                case '4' | 'Flee':
                    if monster.status == 'boss':
                        print('You cannot flee')
                    else:
                        if flee(player):
                            break
                        else:
                            player.action = True
        else:
            print('Unavailable option')

        if player.action:
            if monster.hp <= 0:
                monster_death(player, monster)
                break
            else:
                monster_attacks(player, monster)
                if monster.hp <= 0:
                    monster_death(player, monster)
                    break
                regen(player)
                buff_time(player)

        if player.hp <= 0:
            player.alive = False
            print('You died')
            break

def monster_death(player, monster):
    print('Monster died')
    if player.class_name == 'Mage' and player.shield == 'Mana Shield':
        desactive_mana_shield(player)
    exp_gold_gain(player, monster)
    reset_player_mana(player)
    buff_end_battle(player)


def reset_player_mana(player):
    if player.class_name == 'Rogue':
        player.mana = player.mana_max
    elif player.class_name == 'Warrior':
        player.mana = 0


def regen(player):
    player.hp = min(player.hp + player.hp_regen, player.hp_max)
    if player.class_name in ['Rogue', 'Mage', 'Paladin']:
        player.mana = min(player.mana + player.mana_regen, player.mana_max)
    print(f'\nYou gained {player.mana_regen} {player.resource.upper()} and {player.hp_regen} HP , for your regen')




def exp_gold_gain(player, monster):
    print(f'You received {monster.exp} exp and {monster.gold} gold\n')
    player.gold += monster.gold
    player.exp += int(monster.exp * round(player.exp_multi, 1))
    while True:
        if player.exp >= player.exp_max:
            player.exp -= player.exp_max
            levelup(player)
        else:
            break


def attack(player, monster):
    crit_check = False
    damage = 0

    if player.crit != 0:
        crit_check = critical_check(player)

    match player.class_name:
        case 'Warrior' | 'Paladin':
            damage = round(player.str * (1 - (monster.pdef / 100)))
        case 'Mage':
            damage = round(player.int * (1 - (monster.mdef / 100)))
        case 'Rogue':
            damage = round(player.dex * (1 - (monster.pdef / 100)))

    if crit_check:
        print("Critical damage!")
        print(f"You dealt {damage * 2} damage")
        monster.hp -= damage * 2
        if player.class_name == 'Warrior':
            player.mana = min(player.mana + 10, player.mana_max)
    else:
        print(f"You dealt {damage} damage")
        monster.hp -= damage
        if player.class_name == 'Warrior':
            player.mana = min(player.mana + 5, player.mana_max)

    if monster.hp > 0:
        print(f"The monster has {monster.hp} HP left")
    player.action = True


def use_magic(player, monster):
    while True:
        crit_check = False
        magic_list = {}
        print(f'You have {player.mana} {player.resource}')

        for num, (magic, attributes) in enumerate(player.magics.items(), start=1):
            magic_list[num] = magic
            print(f"{num} - {magic} ->",
                  " | ".join(f"{attribute}:{description}" for attribute, description in attributes.items()))

        choice = input('Choose a magic ("E" or "Exit"): ').capitalize()
        if choice == 'Exit' or choice == 'E':
            break
        elif choice.strip() == '':
            print('Unavailable option')
        elif choice.title() in player.magics.keys() or int(choice) in magic_list:
            if choice.isdigit():
                choice = magic_list[int(choice)]

            if player.mana < player.magics[choice][player.resource]:
                print(f"You do not have enough {player.resource} to use this magic")
            else:
                player.mana -= player.magics[choice][player.resource]
                player.magics[choice]['exp'][0] += int(10 * round(player.exp_multi, 1))
                if "damage" in player.magics[choice]:
                    total = magic_value(player, choice)
                    if player.magics[choice]['type'] == 'physical':
                        total = round(total * (1 - (monster.pdef / 100)))
                    elif player.magics[choice]['type'] == 'magic':
                        total = round(total * (1 - (monster.mdef / 100)))
                    if 'bonus' in player.magics[choice]:
                        match player.magics[choice]['bonus']:
                            case 'lifesteal':
                                print('You used a LIFESTEAL ability and will heal for the damage dealt')
                                player.hp = min(player.hp + total, player.hp_max)
                    if player.crit != 0:
                        crit_check = critical_check(player)
                    if crit_check:
                        print("Critical damage!")
                        print(f"You dealt {total * 2} damage")
                        monster.hp -= total * 2
                    else:
                        print(f"You dealt {total} damage")
                        monster.hp -= total
                    if monster.hp > 0:
                        print(f"The monster has {monster.hp} HP left")
                    if player.class_name == 'Warrior':
                        player.mana = min(player.mana + 5, player.mana_max)

                elif "heal" in player.magics[choice]:
                    total = magic_value(player, choice)
                    if player.crit != 0:
                        crit_check = critical_check(player)
                    if crit_check:
                        print("Critical heal!")
                        print(f"You healed {total * 2} HP")
                        player.hp = min(player.hp + (total * 2), player.hp_max)
                    else:
                        print(f"You healed {total} HP")
                        player.hp = min(player.hp + total, player.hp_max)
                    print(f"You have {player.hp} HP left")

                elif "buff" in player.magics[choice]['type']:
                    buffstats = copy.deepcopy(player.magics[choice])
                    buff_check(player,choice, buffstats)
                    print('@' * 60)
                    print(f'You use {choice.upper()} , granting: ', end='')
                    buff_used(buffstats)
                    print('@' * 60)

                if player.magics[choice]['exp'][0] >= player.magics[choice]['exp'][1]:
                    levelup_magic(player, choice)
                player.action = True
                break
        else:
            print('Unavailable option')

def magic_value(player, choice):
    tooltip = 0
    total = 0
    if 'damage' in player.magics[choice]:
        total = player.magics[choice]["damage"]
    elif 'heal' in player.magics[choice]:
        total = player.magics[choice]["heal"]
    for attribute in player.magics[choice]["tooltip"]:
        match attribute:
            case 'str':
                tooltip += player.str
            case 'dex':
                tooltip += player.dex
            case 'int':
                tooltip += player.int
    total *= tooltip
    return total


def monster_attacks(player, monster):
    if player.dodge > random.choice(dice):
        print("You dodged the attack!")
        if player.class_name == 'Rogue':
            print('You counter-attacked the monster')
            attack(player, monster)
    else:
        crit_check = critical_check(monster)
        damage = round(monster.damage * (1 - (player.pdef / 100)))
        if crit_check:
            final_damage = damage * 2
            print('\nYou received Critical Damage!')
            shield_block(player, final_damage)
        else:
            print()
            shield_block(player, damage)
        if player.hp > 0:
            print(f'You have {player.hp} HP left')

        if player.class_name == 'Warrior':
            if damage / 10 < 5:
                player.mana += 5
            else:
                if int(damage / 10) > 20:
                    player.mana = min(player.mana + 20, player.mana_max)
                else:
                    player.mana = min(player.mana + round(damage / 10), player.mana_max)

def shield_block(player, damage):
    if player.shield == 'Mana Shield':
        reduc = player.magics['Mana Shield']['reduction']
        final_damage = damage * round(1-(reduc/100))
        if player.mana < final_damage:
            print(f"The monster dealt {player.mana} damage to you remaining mana", end=', ')
            player.mana -= final_damage
            leftover_damage = abs(player.mana)
            print(f'and dealt {leftover_damage} to you hp')
            player.mana = max(player.mana, 0)
            player.hp -= leftover_damage
            desactive_mana_shield(player)
        else:
            print(f"The monster dealt {final_damage} damage to you mana")
            player.mana -= final_damage

    else:
        print(f"The monster dealt {damage} damage to you hp")
        player.hp -= damage



def critical_check(npc):
    return npc.crit > random.choice(dice)


def flee(player):
    escape = 50 + player.dodge
    if escape >= random.choice(dice):
        print('You fled successfully')
        buff_end_battle(player)
        return True
    else:
        print('You failed to escape')
        return False