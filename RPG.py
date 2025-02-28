from utility.character import  *
from utility.shop import *
from utility.battle import *

def main():
    player = create_character()
    city = {'1':'Status', '2':'Inn', '3':'Shop', '4':'Battleground', '9':'Quit'}
    while player.alive:
        for num, option in city.items():
            print(f'{num} - {option}')
        choice = input('Choose an option: ').strip().title()

        match choice:
            case '1' | 'Status':
                player.status()

            case '2' | 'Inn':
                choice = input(f"Do you want to pay 20 gold to recover (Y)? GOLD: {player.gold} ")
                if choice.upper() == 'Y':
                    if player.gold < 20:
                        print('Not enough gold to pay')
                    else:
                        player.gold -= 20
                        print('\nYou visited the local inn and recovered from your wounds')
                        player.hp = player.hp_max
                        if player.class_name == 'Mage' or player.class_name == 'Paladin':
                            player.mana = player.mana_max

            case '3' | 'Shop':
                shop(player)

            case '4' | 'Battleground':
                difficulty_list = {"1": "Easy", "2": "Medium", "3": "Hard", "4": "Boss"}
                difficulty = input('Choose the difficulty: (1-Easy | 2-Medium | 3-Hard | 4-Boss): ')
                if difficulty.isdigit() and difficulty in difficulty_list.keys():
                    difficulty = int(difficulty)
                    if difficulty == 4:
                        choice = input('You won\'t be able to flee from the battle, do you really want to face a boss? [Y]').upper()
                        if choice == 'Y':
                            start_battle(player, difficulty)
                    else:
                        start_battle(player, difficulty)
                elif difficulty.capitalize() in difficulty_list.values():
                    key = [key for key, value in difficulty_list.items() if value == difficulty.capitalize()][0]
                    difficulty = int(key)
                    if difficulty == 4:
                        choice = input('You won\'t be able to flee from the battle, do you really want to face a boss? [Y]').upper()
                        if choice == 'Y':
                            start_battle(player, difficulty)
                    else:
                        start_battle(player, difficulty)
                else:
                    print('Difficulty not found')

            case '9' | 'Quit':
                print("Exiting the game...")
                break
            case _:
                print("Invalid option, please try again.")

if __name__ == "__main__":
    main()


