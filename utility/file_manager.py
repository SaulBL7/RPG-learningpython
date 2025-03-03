from .character import *
import json
import os

def save_game(player):
    name = input('Choice your save file name: ')
    location = f'saves/{name}.json'
    if not os.path.exists(location):
        with open(location, 'w') as file:
            json.dump(vars(player), file, ensure_ascii=False, indent=4)
        print('@' * 50)
        print(f"File '{name}' created successfully!")
        print('@' * 50)
    else:
        print(f"The file '{name}' already exists.")
        print('#'*50)
        choice = input('Want to overwrite?(Y)')
        if choice.upper() == 'Y' or choice.upper() == 'Yes':
            with open(location, 'w') as file:
                json.dump(vars(player), file, ensure_ascii=False, indent=4)
            print(f"File '{name}' overwrited successfully!")

def files_load():
    files =[]
    allfiles = {}
    save = 'saves'
    if os.path.exists(save):
        files = [f for f in os.listdir(save) if f.endswith('.json')]
    if files:
        for num , file in enumerate(files):
            allfiles[num] = file.replace('.json', '')
            print(f'{num} - {file.replace('.json', '')}')
    choice = input('Choice a file to loading: ')
    if choice in allfiles.values():
        load = choice
        player = Player.load_game(load)
        return player
    elif int(choice) in allfiles.keys():
        load = allfiles[int(choice)]
        player = Player.load_game(load)
        return player
    else:
        print('File not found')
