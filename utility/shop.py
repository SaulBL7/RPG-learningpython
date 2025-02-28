from .equip import *

def shop(player):
    item_type = {'1': 'Weapon', '2': 'Armor', '3': 'Accessory', '9': 'Exit'}

    while True:
        for num, option in item_type.items():
            print(f'{num} - {option}')
        choice = input('What would you like to buy? ').strip().capitalize()

        match choice:
            case '1' | 'Weapon':
                weapon_shop(player)
            case '2' | 'Armor':
                armor_shop(player)
            case '3' | 'Accessory':
                accessory_shop(player)
            case '9':
                break
            case _:
                print('Invalid option')

def weapon_shop(player):
    gold_value = 0
    weapon_list = {'Axe': {'str': 5, 'crit': 5, 'gold': 50},
                   'Dagger': {'dex': 5, 'crit': 10, 'gold': 50},
                   'Staff': {'int': 5, 'crit': 5, 'gold': 50},
                   'Sword': {'str': 3, 'int': 2, 'crit': 5, 'gold': 50},
                   'Training Sword': {'exp': 1.2, 'gold': 50}
                  }
    while True:
        choice, choice_list = description(weapon_list)
        if choice == 'Exit' or choice == 'E':
            break
        if choice.isdigit():
            choice = int(choice)
        if choice in choice_list:
            choice = choice_list[choice]
            if player.gold >= weapon_list[choice]['gold']:
                if player.weapon == {}:
                    confirm = input(f'Do you want to buy a {choice} costing {weapon_list[choice]["gold"]} gold? [Y]').upper()
                    if confirm == 'Y':
                        player.gold -= weapon_list[choice]['gold']
                        equip_weapon(player, choice, weapon_list[choice])
                        break
                elif list(player.weapon.keys())[0] != choice:
                    confirm = input(f'You have a {list(player.weapon.keys())[0]}, do you want to swap it for a {choice} costing {weapon_list[choice]["gold"]} gold? [Y]').upper()
                    if confirm == 'Y':
                        for item in player.weapon.values():
                            gold_value = int(item.get('gold') / 2)
                        player.gold += gold_value
                        print(f'You received {gold_value} gold for your old weapon')
                        player.gold -= weapon_list[choice]['gold']
                        equip_weapon(player, choice, weapon_list[choice])
                        break
                elif list(player.weapon.keys())[0] == choice:
                    print('You already have this weapon')
            else:
                print('Insufficient gold')
        else:
            print('Invalid option')

def armor_shop(player):
    gold_value = 0
    armor_list = {'Iron Armor': {'hp': 200, 'str': -2, 'dex': -2, 'dodge': -50, 'pdef': 30, 'mdef': -30, 'gold': 100},
                  'Leather Clothes': {'hp': 40, 'energy': 40, 'dex': 2, 'dodge': 20, 'gold': 100},
                  'Cloak': {'hp': 20, 'mana': 100, 'int': 5, 'dodge': 5, 'mdef': 20, 'gold': 100},
                  'Light Armor': {'hp': 50, 'mana': 50, 'str': 2, 'int': 2, 'pdef': 10, 'mdef': 10, 'gold': 100},
                  'Training Clothes': {'hp': 20, 'exp': 1.2, 'gold': 100}
                 }
    while True:
        choice, choice_list = description(armor_list)
        if choice == 'Exit' or choice == 'E':
            break
        if choice.isdigit():
            choice = int(choice)
        if choice in choice_list:
            choice = choice_list[choice]
            if player.gold >= armor_list[choice]['gold']:
                if player.armor == {}:
                    confirm = input(f'Do you want to buy a {choice} costing {armor_list[choice]["gold"]} gold? [Y]').upper()
                    if confirm == 'Y':
                        player.gold -= armor_list[choice]['gold']
                        equip_armor(player, choice, armor_list[choice])
                        break
                elif list(player.armor.keys())[0] != choice:
                    confirm = input(f'You have a {list(player.armor.keys())[0]}, do you want to swap it for a {choice} costing {armor_list[choice]["gold"]} gold? [Y]').upper()
                    if confirm == 'Y':
                        for item in player.armor.values():
                            gold_value = int(item.get('gold') / 2)
                        player.gold += gold_value
                        print(f'You received {gold_value} gold for your old armor')
                        player.gold -= armor_list[choice]['gold']
                        equip_armor(player, choice, armor_list[choice])
                        break
                elif list(player.armor.keys())[0] == choice:
                    print('You already have this armor')
            else:
                print('Insufficient gold')
        else:
            print('Invalid option')

def accessory_shop(player):
    gold_value = 0
    accessory_list = {'STR Ring': {'str': 5, 'gold': 300},
                      'DEX Ring': {'dex': 5, 'gold': 300},
                      'INT Ring': {'int': 5, 'gold': 300},
                      'Weights': {'str': -2, 'dex': -2, 'int': -2, 'exp': 1.2, 'gold': 100}
                     }
    while True:
        choice, choice_list = description(accessory_list)
        if choice == 'Exit' or choice == 'E':
            break
        if choice.isdigit():
            choice = int(choice)
        if choice in choice_list:
            choice = choice_list[choice]
            if player.gold >= accessory_list[choice]['gold']:
                if player.trinket == {}:
                    confirm = input(f'Do you want to buy a {choice} costing {accessory_list[choice]["gold"]} gold? [Y]').upper()
                    if confirm == 'Y':
                        player.gold -= accessory_list[choice]['gold']
                        equip_trinket(player, choice, accessory_list[choice])
                        break
                elif list(player.trinket.keys())[0] != choice:
                    confirm = input(f'You have a {list(player.trinket.keys())[0]}, do you want to swap it for a {choice} costing {accessory_list[choice]["gold"]} gold? [Y]').upper()
                    if confirm == 'Y':
                        for item in player.trinket.values():
                            gold_value = int(item.get('gold') / 2)
                        player.gold += gold_value
                        print(f'You received {gold_value} gold for your old accessory')
                        player.gold -= accessory_list[choice]['gold']
                        equip_trinket(player, choice, accessory_list[choice])
                        break
                elif list(player.trinket.keys())[0] == choice:
                    print('You already have this accessory')
            else:
                print('Insufficient gold')
        else:
            print('Invalid option')

def description(itens):
    choice_list = {}
    for num, stats in enumerate(itens.keys()):
        print(f"{num + 1} - {stats} ->", end=' ')
        for desc in itens[stats].keys():
            match desc:
                case 'hp':
                    print(f"HP: {itens[stats][desc]}", end=' | ')
                case 'mana':
                    print(f"Mana: {itens[stats][desc]}", end=' | ')
                case 'str':
                    print(f"STR: {itens[stats][desc]}", end=' | ')
                case 'dex':
                    print(f"DEX: {itens[stats][desc]}", end=' | ')
                case 'int':
                    print(f"INT: {itens[stats][desc]}", end=' | ')
                case 'crit':
                    print(f"CRIT: {itens[stats][desc]}%", end=' | ')
                case 'pdef':
                    print(f"PHYSICAL DEFENSE: {itens[stats][desc]}%", end=' | ')
                case 'mdef':
                    print(f"MAGIC DEFENSE: {itens[stats][desc]}%", end=' | ')
                case 'dodge':
                    print(f"Dodge: {itens[stats][desc]}%", end=' | ')
                case 'exp':
                    print(f"EXP Multiplier: {itens[stats][desc]}", end=' | ')
                case 'gold':
                    print(f"Cost:  {itens[stats][desc]} gold")
        choice_list[num + 1] = stats
    choice = input('Which accessory would you like to buy? ("Exit" or "E")')
    return choice , choice_list
