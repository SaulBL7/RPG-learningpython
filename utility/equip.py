def equip_weapon(player, new_weapon, stats):
    if player.weapon != {}:
        old_weapon = list(player.weapon.keys())[0]
        for attribute, value in player.weapon[old_weapon].items():
            match attribute:
                case 'str':
                    player.str -= value
                case 'dex':
                    player.dex -= value
                case 'int':
                    player.int -= value
                case 'crit':
                    player.crit -= value
                case 'exp':
                    player.exp_multi -= value - 1

    player.weapon = {new_weapon: stats}

    for attribute, value in stats.items():
        match attribute:
            case 'str':
                player.str += value
            case 'dex':
                player.dex += value
            case 'int':
                player.int += value
            case 'crit':
                player.crit += value
            case 'exp':
                player.exp_multi += value - 1
    print('@'* 40)
    print(f'Weapon equipped: {new_weapon}')
    print(f'HP: {player.hp}/{player.hp_max} | {player.resource.upper()}: {player.mana}/{player.mana_max}')
    print(f'Strength: {player.str} | Dexterity: {player.dex} | Intelligence: {player.int}')
    print(f'Critical: {player.crit}% | PDEF: {player.pdef}% | MDEF: {player.mdef}% | Dodge: {player.dodge}%')
    print('@' * 40)

def equip_armor(player, new_armor, stats):
    if player.armor != {}:
        old_armor = list(player.armor.keys())[0]
        for attribute, value in player.armor[old_armor].items():
            match attribute:
                case 'hp':
                    player.hp_max -= value
                    if player.hp > player.hp_max:
                        player.hp = player.hp_max
                case 'mana' | 'energy':
                    player.mana_max -= value
                    if player.mana > player.mana_max:
                        player.mana = player.mana_max
                case 'str':
                    player.str -= value
                case 'dex':
                    player.dex -= value
                case 'int':
                    player.int -= value
                case 'crit':
                    player.crit -= value
                case 'dodge':
                    player.dodge -= value
                case 'pdef':
                    player.pdef -= value
                case 'mdef':
                    player.mdef -= value
                case 'exp':
                    player.exp_multi -= value - 1

    player.armor = {new_armor: stats}

    for attribute, value in stats.items():
        match attribute:
            case 'hp':
                player.hp_max += value
                player.hp += value
            case 'mana' | 'energy' if player.resource in [attribute]:
                player.mana_max += value
                player.mana += value
            case 'str':
                player.str += value
            case 'dex':
                player.dex += value
            case 'int':
                player.int += value
            case 'crit':
                player.crit += value
            case 'dodge':
                player.dodge += value
            case 'pdef':
                player.pdef += value
            case 'mdef':
                player.mdef += value
            case 'exp':
                player.exp_multi += value - 1

    print('@' * 40)
    print(f'Armor equipped: {new_armor}')
    print(f'HP: {player.hp}/{player.hp_max} | {player.resource.upper()}: {player.mana}/{player.mana_max}')
    print(f'Strength: {player.str} | Dexterity: {player.dex} | Intelligence: {player.int}')
    print(f'Critical: {player.crit}% | PDEF: {player.pdef}% | MDEF: {player.mdef}% | Dodge: {player.dodge}%')
    print('@' * 40)

def equip_trinket(player, new_trinket, stats):
    if player.trinket != {}:
        old_item = list(player.trinket.keys())[0]
        for attribute, value in player.trinket[old_item].items():
            match attribute:
                case 'hp':
                    player.hp_max -= value
                    if player.hp > player.hp_max:
                        player.hp = player.hp_max
                case 'mana' | 'energy':
                    player.mana_max -= value
                    if player.mana > player.mana_max:
                        player.mana = player.mana_max
                case 'str':
                    player.str -= value
                case 'dex':
                    player.dex -= value
                case 'int':
                    player.int -= value
                case 'crit':
                    player.crit -= value
                case 'dodge':
                    player.dodge -= value
                case 'exp':
                    player.exp_multi -= value - 1

    player.trinket = {new_trinket: stats}

    for attribute, value in stats.items():
        match attribute:
            case 'hp':
                player.hp_max += value
                player.hp += value
            case 'mana' | 'energy' if player.resource in [attribute]:
                player.mana_max += value
                player.mana += value
            case 'str':
                player.str += value
            case 'dex':
                player.dex += value
            case 'int':
                player.int += value
            case 'crit':
                player.crit += value
            case 'dodge':
                player.dodge += value
            case 'exp':
                value -= 1
                player.exp_multi += value

    print('@' * 40)
    print(f'Trinket equipped: {new_trinket}')
    print(f'HP: {player.hp}/{player.hp_max} | {player.resource.upper()}: {player.mana}/{player.mana_max}')
    print(f'Strength: {player.str} | Dexterity: {player.dex} | Intelligence: {player.int}')
    print(f'Critical: {player.crit}% | PDEF: {player.pdef}% | MDEF: {player.mdef}% | Dodge: {player.dodge}%')
    print('@' * 40)
