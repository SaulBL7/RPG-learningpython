import random
from .levelup import *

dice = []
for i in range(1, 100):
    dice.append(i)


class Monster:
    def __init__(self, player, difficulty):
        match difficulty:
            case 1:
                self.level = player.level
            case 2:
                self.level = player.level + 1
            case 3:
                self.level = player.level + random.randint(2, 3)
            case 4:
                self.level = player.level + 5

        self.name = f"Monster {self.level}"
        if difficulty == 4:
            self.damage = 6 * self.level
            self.hp = self.hp_max = 60 * self.level
            self.crit = 10 + (self.level / 2)
            self.exp = 500 * self.level
            self.gold = 50 * self.level
            self.pdef = 20
            self.mdef = 20
            self.status = 'boss'
        else:
            self.damage = 4 * self.level
            self.hp = self.hp_max = 40 * self.level
            self.crit = 10 * (self.level / 2)
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
        available_choices = {"1": "Attack", "2": "Magic", "3": "Flee"}
        print("-" * 30)
        print(
            f'{player.name} -> HP: {player.hp}/{player.hp_max} | {player.resource.upper()}: {player.mana}/{player.mana_max}')
        print(f'MONSTER -> HP: {monster.hp}/{monster.hp_max} | Damage: {monster.damage}')
        print("-" * 30)
        choice = input("Choose an action (1-Attack|2-Magic|3-Flee): ").capitalize()

        if choice in available_choices or choice in available_choices.values():
            choice = available_choices.get(choice, choice)
            match choice:
                case '1' | 'Attack':
                    attack(player, monster)
                    player.action = True
                case '2' | 'Magic':
                    use_magic(player, monster)
                case '3' | 'Flee':
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
                print('Monster died')
                exp_gold_gain(player, monster)
                if player.class_name == 'Rogue':
                    player.mana = player.mana_max
                elif player.class_name == 'Warrior':
                    player.mana = 0
                break
            else:
                monster_attacks(player, monster)
                if monster.hp <= 0:
                    print('Monster died')
                    exp_gold_gain(player, monster)
                    if player.class_name == 'Rogue':
                        player.mana = player.mana_max
                    elif player.class_name == 'Warrior':
                        player.mana = 0
                    break
                regen(player)

        if player.hp <= 0:
            player.alive = False
            print('You died')
            break


def regen(player):
    match player.class_name:
        case 'Rogue':
            player.mana += player.mana_regen
            if player.mana > player.mana_max:
                player.mana = player.mana_max
        case 'Mage' | 'Paladin':
            player.mana += player.mana_regen
            if player.mana > player.mana_max:
                player.mana = player.mana_max
        case 'Warrior':
            player.hp += player.hp_regen
            if player.hp > player.hp_max:
                player.hp = player.hp_max


def exp_gold_gain(player, monster):
    print(f'You received {monster.exp} exp and {monster.gold} gold')
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
            damage = round(player.strength * (1 - (monster.pdef / 100)))
        case 'Mage':
            damage = round(player.intelligence * (1 - (monster.mdef / 100)))
        case 'Rogue':
            damage = round(player.dexterity * (1 - (monster.pdef / 100)))

    if crit_check:
        print("Critical damage!")
        print(f"You dealt {damage * 2} damage")
        monster.hp -= damage * 2
        if player.class_name == 'Warrior':
            player.mana += 10
            if player.mana > player.mana_max:
                player.mana = player.mana_max
    else:
        print(f"You dealt {damage} damage")
        monster.hp -= damage
        if player.class_name == 'Warrior':
            player.mana += 5
            if player.mana > player.mana_max:
                player.mana = player.mana_max

    if monster.hp > 0:
        print(f"The monster has {monster.hp} HP left")
    player.action = True


def use_magic(player, monster):
    while True:
        crit_check = False
        magic_list = {}
        tooltip = 0
        print(f'You have {player.mana} {player.resource}')

        for num, (magic, attributes) in enumerate(player.magics.items(), start=1):
            magic_list[num] = magic
            print(f"{num} - {magic} ->",
                  " | ".join(f"{attribute}:{description}" for attribute, description in attributes.items()))

        choice = input('Choose a magic ("S" or "Exit"): ').capitalize()
        if choice == 'Exit' or choice == 'S':
            break
        elif choice.title() in player.magics.keys() or int(choice) in magic_list:
            if choice.isdigit():
                choice = magic_list[int(choice)]

            if player.mana < player.magics[choice][player.resource]:
                print(f"You do not have enough {player.resource} to use this magic")
            else:
                player.mana -= player.magics[choice][player.resource]
                player.magics[choice]['exp'][0] += int(10 * round(player.exp_multi, 1))
                if "damage" in player.magics[choice]:
                    total = player.magics[choice]["damage"]
                    for attribute in player.magics[choice]["tooltip"]:
                        match attribute:
                            case 'strength':
                                tooltip += player.strength
                            case 'dexterity':
                                tooltip += player.dexterity
                            case 'intelligence':
                                tooltip += player.intelligence
                    total *= tooltip
                    if player.magics[choice]['type'] == 'physical':
                        total = round(total * (1 - (monster.pdef / 100)))
                    elif player.magics[choice]['type'] == 'magic':
                        total = round(total * (1 - (monster.mdef / 100)))
                    if 'bonus' in player.magics[choice]:
                        match player.magics[choice]['bonus']:
                            case 'lifesteal':
                                print('You used a LIFESTEAL ability and will heal for the damage dealt')
                                player.hp += total
                                if player.hp > player.hp_max:
                                    player.hp = player.hp_max
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
                        player.mana += 5
                        if player.mana > player.mana_max:
                            player.mana = player.mana_max


                elif "heal" in player.magics[choice]:
                    total = player.magics[choice][player.resource]
                    for attribute in player.magics[choice]["tooltip"]:
                        match attribute:
                            case 'strength':
                                tooltip += player.strength
                            case 'dexterity':
                                tooltip += player.dexterity
                            case 'intelligence':
                                tooltip += player.intelligence
                    total *= tooltip
                    if player.crit != 0:
                        crit_check = critical_check(player)
                    if crit_check:
                        print("Critical heal!")
                        print(f"You healed {total * 2} HP")
                        player.hp += total * 2
                    else:
                        print(f"You healed {total} HP")
                        player.hp += total
                    if player.hp > player.hp_max:
                        player.hp = player.hp_max
                    print(f"You have {player.hp} HP left")
                if player.magics[choice]['exp'][0] >= player.magics[choice]['exp'][1]:
                    levelup_magic(player, choice)
                player.action = True
                break
        else:
            print('Unavailable option')


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
            print('\nYou received Critical Damage!')
            print(f"The monster dealt {damage * 2} damage to you")
            player.hp -= damage * 2
        else:
            print(f"\nThe monster dealt {damage} damage to you")
            player.hp -= damage
        if player.hp > 0:
            print(f'You have {player.hp} HP left')

        if player.class_name == 'Warrior':
            if damage / 10 < 5:
                player.mana += 5
            else:
                if int(damage / 10) > 20:
                    player.mana += 20
                else:
                    player.mana += int(damage / 10)
                if player.mana > player.mana_max:
                    player.mana = player.mana_max


def critical_check(npc):
    if npc.crit > random.choice(dice):
        return True
    else:
        return False


def flee(player):
    escape = 50 + player.dodge
    if escape >= random.choice(dice):
        print('You fled successfully')
        return True
    else:
        print('You failed to escape')
        return False