import random
from .equip import *

attributes = ['hp','hp_regen','mana_regen','mana','str','int','dex','dodge','pdef','mdef','crit']
items = ['Weapon','Armor','Accessory']

def item_enchant(player):
    while True:
        for i, item in enumerate(items):
            print(f'{i+1} - {item}')
        choice = input('Which item do you want to enchant? [E to Exit]').capitalize()
        match choice.capitalize():
            case '1' | 'Weapon':
                choice = 'weapon'
                enchant_roll(player, choice)
            case '2' | 'Armor':
                choice = 'armor'
                enchant_roll(player, choice)
            case '3' | 'Accessory' | 'Acc':
                choice = 'trinket'
                enchant_roll(player, choice)
            case 'E' | 'Exit':
                break
            case _:
                print('Invalid option')

def enchant_roll(player, choice):
    enchant_cost = player.level * 100
    print(f'{enchant_cost} gold will be needed to choose a random attribute and value to assign to your {choice} ')
    confirm = input('Do you want to confirm the draw? [Y]')
    if player.gold < enchant_cost:
        print('Insufficient gold')
    else:
        if confirm.capitalize() in ['Y','Yes']:
            player.gold -= enchant_cost
            value = 0

            draw = random.choice(attributes)

            match draw:
                case 'hp' | 'mana':
                    value = random.randint(50, 200)
                case 'hp_regen' | 'mana_regen':
                    value = random.randint(5, 20)
                case 'str' | 'dex' | 'int' | 'pdef' | 'mdef' | 'dodge' | 'crit' :
                    value = random.randint(1, 5)

            confirm = input(f'Want to enchant the {choice.capitalize()} with {draw.upper()}: +{value} ? [Y]')
            if confirm.capitalize() in ['Y', 'Yes']:
                match choice:

                    case 'weapon':
                        item = list(player.weapon.keys())[0]
                        if draw in player.weapon[item]:
                            player.weapon[item][draw] += value
                        else:
                            player.weapon[item][draw] = value
                        if not item.lower().startswith("enchanted"):
                            new_name = f"Enchanted {item.title()}+1"
                            player.weapon[new_name] = player.weapon.pop(item)

                    case 'armor':
                        item = list(player.armor.keys())[0]
                        if draw in player.armor[item]:
                            player.armor[item][draw] += value
                        else:
                            player.armor[item][draw] = value
                        if not item.lower().startswith("enchanted"):
                            new_name = f"Enchanted {item.title()}"
                            player.armor[new_name] = player.armor.pop(item)

                    case 'trinket':
                        item = list(player.trinket.keys())[0]
                        if draw in player.trinket[item]:
                            player.trinket[item][draw] += value
                        else:
                            player.trinket[item][draw] = value
                        if not item.lower().startswith("enchanted"):
                            new_name = f"Enchanted {item.title()}"
                            player.trinket[new_name] = player.trinket.pop(item)

                plus_stats(player, draw, value)
                print(f'Successful enchanting {choice.upper()}')





