
def buff_check(player,choice,stats):
    if choice in player.buffs:
        player.buffs[choice]['time'] = 5
    else:
        player.buffs[choice] = stats
        buff_plus(player, player.buffs[choice])

def buff_plus(player,buff):
    for atribute in buff:
        match atribute:
            case 'pdef':
                player.pdef += buff['pdef']
            case 'mdef':
                player.mdef += buff['mdef']

def buff_minus(player,remove_buffs):
    for buff in remove_buffs:
        for atribute in player.buffs[buff]:
            match atribute:
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
            case 'pdef':
                print(f'PDEF: +{value}', end=' | ')
            case 'mdef':
                print(f'MDEF: +{value}')

