def levelup(player):
    player.level += 1
    player.exp_max = round(player.exp_max * 1.3)
    match player.class_name:
        case 'Warrior':
            player.hp_max += 50
            player.hp = player.hp_max
            player.str += 3

        case 'Mage':
            player.hp_max += 20
            player.hp = player.hp_max
            player.mana_max += 50
            player.mana = player.mana_max
            player.int += 3

        case 'Rogue':
            player.hp_max += 30
            player.hp = player.hp_max
            player.dex += 3

        case 'Paladin':
            player.hp_max += 40
            player.hp = player.hp_max
            player.mana_max += 15
            player.mana = player.mana_max
            if player.level % 2 == 0:
                player.str += 2
                player.int += 1
            else:
                player.str += 1
                player.int += 2
    gain_magic(player)

    print(f'\nYou leveled up to level {player.level}!!')
    print('-' * 30)
    print(f'Character: {player.name} | Class: {player.class_name} | Level: {player.level}')
    print(f'HP: {player.hp}/{player.hp_max} | {player.resource.upper()}: {player.mana}/{player.mana_max}')
    print(f'Strength: {player.str} | Dexterity: {player.dex} | Intelligence: {player.int}')
    print(f'EXP: {player.exp}/{player.exp_max}')
    print('-' * 30)

def levelup_magic(player, choice):
    print('#' * 30)
    if 'damage' in player.magics[choice]:
        player.magics[choice]['level'] += 1
        player.magics[choice]['damage'] += 1
        if 'mana' in player.magics[choice]:
            player.magics[choice]['mana'] += 2
        player.magics[choice]['exp'][0] -= player.magics[choice]['exp'][1]
        player.magics[choice]['exp'][1] += 10 * (player.magics[choice]['level'] - 1 )
        print(f"Your spell {choice} leveled up to level {player.magics[choice]['level']}")
        print(f"Now it has {player.magics[choice]['damage']} base damage")

    elif 'heal' in player.magics[choice]:
        player.magics[choice]['level'] += 1
        player.magics[choice]['heal'] += 1
        player.magics[choice]['mana'] += 2
        player.magics[choice]['exp'][0] -= player.magics[choice]['exp'][1]
        player.magics[choice]['exp'][1] += 10 * (player.magics[choice]['level'] - 1 )
        print(f"Your spell {choice} leveled up to level {player.magics[choice]['level']}")
        print(f"Now it has {player.magics[choice]['heal']} base healing")

    elif 'buff' in player.magics[choice]:
        player.magics[choice]['level'] += 1
        player.magics[choice]['mana'] += 2
        if 'pdef' in player.magics[choice]:
            player.magics[choice]['pdef'] += 1
        if 'mdef' in player.magics[choice]:
            player.magics[choice]['mdef'] += 1
        player.magics[choice]['exp'][0] -= player.magics[choice]['exp'][1]
        player.magics[choice]['exp'][1] += 10 * (player.magics[choice]['level'] - 1 )
        print(f"Your spell {choice} leveled up to level {player.magics[choice]['level']}")
        print(f"Now it has more buffs")
    print('#' * 30)

def gain_magic(player):
    match player.class_name:
        case 'Mage':
            match player.level:
                case 3:
                    player.magics["Ice Arrow"] = {"level": 1,"type":"magic","mana": 15,"tooltip": ['int'],"damage": 7,"exp": [0,30]}
                    print('%' * 30)
                    print('You learned the spell "ICE ARROW"')
                    print('%' * 30)
                case 5:
                    player.magics["Inferno"] = {"level": 1,"type":"magic","mana": 50,"tooltip": ['int'],"damage": 15,"exp": [0,30]}
                    print('%' * 30)
                    print('You learned the spell "INFERNO"')
                    print('%' * 30)
        case 'Paladin':
            match player.level:
                case 3:
                    player.magics["Consecration"] = {"level": 1,"type":"magic", "mana": 15, "tooltip": ['int'], "damage": 6,"exp": [0, 30]}
                    print('%' * 30)
                    print('You learned the spell "CONSECRATION"')
                    print('%' * 30)
                case 5:
                    player.magics["Bastian"] = {"level": 1, "type": "buff", "mana": 30,"pdef": 15,"mdef":15,"time":5, "exp": [0, 30]}
                    print('%' * 30)
                    print('You learned the spell "BASTIAN"')
                    print('%' * 30)
                case 7:
                    player.magics["Judgment"] = {"level": 1,"type":"physical", "mana": 40, "tooltip": ['str','int'], "damage": 10, "exp": [0, 30]}
                    print('%' * 30)
                    print('You learned the spell "JUDGMENT"')
                    print('%' * 30)
        case 'Warrior':
            match player.level:
                case 3:
                    player.magics["Fierce Strike"] = {"level": 1,"type":"physical", "rage": 40, "tooltip": ['str'], "damage": 10,"exp": [0, 30]}
                    print('%' * 30)
                    print('You learned the spell "FIERCE STRIKE"')
                    print('%' * 30)
                case 5:
                    player.magics["Bloody Strike"] = {"level": 1,"type":"physical", "rage": 50, "tooltip": ['str'], "damage": 10,'bonus':'lifesteal',"exp": [0, 30]}
                    print('%' * 30)
                    print('You learned the spell "BLOODY STRIKE"')
                    print('%' * 30)
        case 'Rogue':
            match player.level:
                case 3:
                    player.magics["Stab"] = {"level": 1,"type":"physical", "energy": 50, "tooltip": ['dex'], "damage": 6,"exp": [0, 30]}
                    print('%' * 30)
                    print('You learned the spell "STAB"')
                    print('%' * 30)
                case 5:
                    player.magics["Double Strike"] = {"level": 1,"type":"physical", "energy": 80, "tooltip": ['dex'], "damage": 10,"exp": [0, 30]}
                    print('%' * 30)
                    print('You learned the spell "DOUBLE STRIKE"')
                    print('%' * 30)