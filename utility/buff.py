buffs_time = {'Bastian': 5,'Warcry': 5,'Vanish': 5, 'Arcane Amplification':5, 'Mana Shield': 99}


def buff_check(player,choice,stats):
    if choice in player.buffs:
        player.buffs[choice]['time'] = buffs_time.get(choice)
    else:
        player.buffs[choice] = stats
        buff_plus(player, player.buffs[choice])
    if choice == 'Mana Shield':
        active_shield(player, choice)

def buff_plus(player,buff):
    for atribute in buff:
        match atribute:
            case 'str':
                player.str += buff['str']
            case 'int':
                player.int += buff['int']
            case 'dodge':
                player.dodge += buff['dodge']
            case 'pdef':
                player.pdef += buff['pdef']
            case 'mdef':
                player.mdef += buff['mdef']

def buff_minus(player,remove_buffs):
    for buff in remove_buffs:
        for atribute in player.buffs[buff]:
            match atribute:
                case 'str':
                    player.str -= player.buffs[buff]['str']
                case 'int':
                    player.int -= player.buffs[buff]['int']
                case 'dodge':
                    player.dodge -= player.buffs[buff]['dodge']
                case 'pdef':
                    player.pdef -= player.buffs[buff]['pdef']
                case 'mdef':
                    player.mdef -= player.buffs[buff]['mdef']
        player.buffs.pop(buff)

def buff_time(player):
    remove_buffs = []
    for buff in player.buffs:
        player.buffs[buff]['time'] -= 1
        if player.buffs[buff]['time'] == 0:
            print('@' * 60)
            print(f'{buff.upper()} effect is over')
            print('@' * 60)
            remove_buffs.append(buff)
    buff_minus(player, remove_buffs)

def buff_end_battle(player):
    remove_buffs = []
    if player.buffs == {}:
        return
    else:
        for buff in player.buffs.keys():
            remove_buffs.append(buff)
        buff_minus(player, remove_buffs)

def buff_used(buff):
    for atribute, value in buff.items():
        match atribute:
            case 'str':
                print(f'STR: +{value}', end=' | ')
            case 'int':
                print(f'INT: +{value}', end=' | ')
            case 'dodge':
                print(f'DODGE: +{value}%', end=' | ')
            case 'pdef':
                print(f'PDEF: +{value}%', end=' | ')
            case 'mdef':
                print(f'MDEF: +{value}%', end=' | ')
            case 'reduction':
                print(f'REDUC: +{value}%', end=' | ')
    print()

def active_shield(player, choice):
    player.shield = choice

def desactive_mana_shield(player):
    player.shield = None
    player.buffs.pop('Mana Shield')
