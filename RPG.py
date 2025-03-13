from utility.shop import *
from utility.battle import *
from utility.file_manager import *
from utility.character import *
from utility.enchant import *


def main():
    while True:
        menu = {'1': 'New game', '2': 'Load game'}
        for num, option in menu.items():
            print(f'{num} - {option}')
        choice = input('Choose an option: ').lower()

        match choice:
            case '1' | 'new game':
                player = create_character()
                break
            case '2' | 'load game':
                player = files_load()
                if player:
                    break
            case _:
                print("Invalid option, please try again.")
    return player

def city(player):

    city = {'1':'Status', '2':'Inn', '3':'Shop','4':'Item Enchanter', '5':'Battleground','8':'Save game','9':'Quit'}
    while player.alive:
        for num, option in city.items():
            print(f'{num} - {option}')
        choice = input('Choose an option: ').strip().title()

        match choice:
            case '1' | 'Status':
                player.status()

            case '2' | 'Inn':
                choice = input(f"Do you want to pay {player.level * 20} gold to recover (Y)? GOLD: {player.gold} ")
                if choice.upper() == 'Y':
                    if player.gold < (player.level * 20):
                        print('Not enough gold to pay')
                    else:
                        player.gold -= (player.level * 20)
                        print('\nYou visited the local inn and recovered from your wounds')
                        player.hp = player.hp_max
                        if player.class_name == 'Mage' or player.class_name == 'Paladin':
                            player.mana = player.mana_max

            case '3' | 'Shop':
                shop(player)

            case '4' | 'Item Enchanter':
                item_enchant(player)

            case '5' | 'Battleground':
                difficulty_list = {"1": "Easy", "2": "Medium", "3": "Hard", "4": "Boss"}
                difficulty = input('Choose the difficulty: (1-Easy | 2-Medium | 3-Hard | 4-Boss): ')
                if difficulty.capitalize() in difficulty_list.values() or difficulty in difficulty_list.keys():
                    if difficulty == "4" or difficulty == "Boss":
                        choice = input('You won\'t be able to flee from the battle, do you really want to face a boss? [Y]').upper()
                        if choice == 'Y':
                            start_battle(player, difficulty)
                    else:
                        start_battle(player, difficulty)
                else:
                    print('Difficulty not found')

            case '8' | 'Save game':
                save_game(player)

            case '9' | 'Quit':
                print("Exiting the game...")
                break

            case _:
                print("Invalid option, please try again.")

if __name__ == "__main__":
    player = main()
    city(player)


