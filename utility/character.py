attribute = {
            "Warrior": {"hp": 100, "rage": 100, "str": 12, "dex": 4, "int": 2, "crit": 5, "pdef": 20, "mdef": 0, "dodge": 0, "desc": "Deals a lot of physical damage with 'RAGE' mechanics, where he gains rage by dealing or receiving damage"},
            "Mage": {"hp": 60, "mana": 100, "str": 2, "dex": 4, "int": 12, "crit": 5, "pdef": 0, "mdef": 20, "dodge": 5, "desc": "Deals a lot of magical damage"},
            "Rogue": {"hp": 80, "energy": 100, "str": 3, "dex": 12, "int": 3, "crit": 30, "pdef": 0, "mdef": 0, "dodge": 20, "desc": "Deals physical damage with 'Energy' mechanics, gaining over time in battle, and when dodging an enemy attack, counterattacks"},
            "Paladin": {"hp": 100, "mana": 50, "str": 8, "dex": 2, "int": 8, "crit": 10, "pdef": 10, "mdef": 10, "dodge": 0, "desc": "Hybrid class with both physical and magical power"},
        }
init_magics =  {
            "Mage": {"Fireball": {"level": 1, "type": "magic", "mana": 10, "tooltip": ['int'], "damage": 4, "exp": [0, 30]}},
            "Warrior": {"Power Strike": {"level": 1, "type": "physical", "rage": 20, "tooltip": ['str'], "damage": 4, "exp": [0, 30]}},
            "Rogue": {"Backstab": {"level": 1, "type": "physical", "energy": 50, "tooltip": ['dex'], "damage": 3, "exp": [0, 30]}},
            "Paladin": {"Smite": {"level": 1, "type": "physical", "mana": 10, "tooltip": ['int', 'str'], "damage": 2, "exp": [0, 30]},
                        "Heal": {"level": 1, "mana": 10, "tooltip": ['int'], "heal": 3, "exp": [0, 30]}}
        }


class Player:
    def __init__(self, name, class_name):
        self.name = name
        self.class_name = class_name
        self.level = 1
        self.exp = 0
        self.exp_max = 100
        self.gold = 1000
        self.weapon = {}
        self.armor = {}
        self.trinket = {}
        self.alive = True
        self.action = False
        self.hp_regen = 0
        self.mana_regen = 0
        self.exp_multi = 1

        if class_name in attribute:
            self.hp = self.hp_max = attribute[class_name]["hp"]
            if "mana" in attribute[class_name]:
                self.mana = self.mana_max = attribute[class_name]["mana"]
                self.resource = 'mana'
                if self.class_name == 'Mage':
                    self.mana_regen = 10
                else:
                    self.mana_regen = 5
            elif "rage" in attribute[class_name]:
                self.mana = 0
                self.mana_max = attribute[class_name]["rage"]
                self.resource = 'rage'
                self.hp_regen = 5
            elif "energy" in attribute[class_name]:
                self.mana = self.mana_max = attribute[class_name]["energy"]
                self.resource = 'energy'
                self.mana_regen = 20
            self.str = attribute[class_name]["str"]
            self.dex = attribute[class_name]["dex"]
            self.int = attribute[class_name]["int"]
            self.crit = attribute[class_name]["crit"]
            self.dodge = attribute[class_name]["dodge"]
            self.pdef = attribute[class_name]["pdef"]
            self.mdef = attribute[class_name]["mdef"]
            self.magics = init_magics[class_name]
        else:
            raise ValueError("Invalid class!\n")

    def status(self):
        print('--------------------------------------------------------------------')
        print(f'Character: {self.name} | Class: {self.class_name} | Level: {self.level}')
        print(f'HP: {self.hp}/{self.hp_max} | {self.resource.capitalize()}: {self.mana}/{self.mana_max}')
        print(f'Strength: {self.str} | Dexterity: {self.dex} | Intelligence: {self.int}')
        print(f'Crit: {self.crit}% | P.DEF: {self.pdef}% | M.DEF: {self.mdef}% | Dodge: {self.dodge}%')
        print(f'EXP: {self.exp}/{self.exp_max} | Gold: {self.gold}')
        if self.weapon == {}:
            print('Weapon: None equipped')
        else:
            item = list(self.weapon.keys())[0]
            print(f'Weapon: {item}', end='->')
            for stats, value in self.weapon[item].items():
                if stats != 'gold':
                    print(f' {stats.upper()} : {value}', end='  |  ')
            print('')
        if self.armor == {}:
            print('Armor: None equipped')
        else:
            item = list(self.armor.keys())[0]
            print(f'Armor: {item}', end='->')
            for stats, value in self.armor[item].items():
                if stats != 'gold':
                    print(f' {stats.upper()} : {value}', end='  |  ')
            print('')
        if self.trinket == {}:
            print('Accessory: None equipped')
        else:
            item = list(self.trinket.keys())[0]
            print(f'Accessory: {item}', end='->')
            for stats, value in self.trinket[item].items():
                if stats != 'gold':
                    print(f' {stats.upper()} : {value}', end='  |  ')
        print('\n--------------------------------------------------------------------')
        print('Spells')
        for spell, attributes in self.magics.items():
            print(f"{spell} ->", " | ".join(f"{attribute}: {descr}" for attribute, descr in attributes.items()))
        print('--------------------------------------------------------------------')

def create_character():
    name = input('Enter your character\'s name: ').title()

    available_classes = {"1": "Warrior", "2": "Rogue", "3": "Mage", "4": "Paladin"}

    while True:
        print('Available classes:')
        for num, class_name in available_classes.items():
            print(f'{num} - {class_name}')
        choice = input('What is your class? ').strip().capitalize()

        if choice in available_classes or choice in available_classes.values():
            selected_class = available_classes.get(choice, choice)
            print(f"{attribute[selected_class]['desc']}")
            confirmation = input(f"Confirm selection as '{selected_class}'? (Y/N) ").strip().upper()
            if confirmation == 'Y':
                return Player(name, selected_class)
        else:
            print('Class not available, please try again.')