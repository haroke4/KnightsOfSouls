"""
Вся инфа про боссов, персов
"""


def increase_mob_characteristics(x):
    for i in [mini_golem, snake, ice_soul, fire_soul, dog, tree, dragonboss, necroboss, hunter, golem]:
        i["hp"] = x * i["hp"]
        i["armor"] = x * i["armor"]
        i["damage"] = x * i["damage"]
        i["protection"] = x * i["protection"]


# HEROES
spearman = {
    "name": "Копейщик",
    "img": "SpearMan/down/1.png",
    "gun_img": "arrow.png",
    "hp": 6,
    "armor": 5,
    "protection": 0,
    "walk_speed": 1.25,
    "run_speed": 2.5,
    "attack_cooldown": 1,
    "damage": 7,
    "description": "Метает копья, 10% шанс поставить трипл урон"
}
magicman = {
    "name": "Ледяной колдун",
    "img": "MagicMan/down/1.png",
    "gun_img": "magicman_fire.png",
    "hp": 7,
    "armor": 7,
    "protection": 0,
    "walk_speed": 1.0,
    "run_speed": 1.75,
    "attack_cooldown": 2,
    "damage": 5,
    "description": "Создает ледяные шипы  из земли, враги замедляются при попаданий",
    "attack_range": 500
}
swordman = {
    "name": "Фихтовальщик",
    "img": "SwordMan/down/1.png",
    "gun_img": "sword.png",
    "hp": 5,
    "armor": 10,
    "protection": 1,
    "walk_speed": 1.0,
    "run_speed": 2.0,
    "attack_cooldown": 0.5,
    "damage": 5,
    "description": "Мастер ближнего боя - в совершенстве владеет рапирой, которой наносит проникающие удары. Носит "
                   "свою тренировочную броню, из-за чего получает на 1 меньше урона из любого источника. "
}

# ENEMY
snake = {
    "name": "Ядовитая Змея",
    "img": "abobus.png",
    "hp": 1,
    "armor": 0,
    "protection": 0,
    "speed": 3,
    "attack_cooldown": 2,
    "damage": 1,
    "attack_distance": 50,
}

mini_golem = {
    "name": "Мини-голем",
    "img": "Mini-golem/walk-left/1.png",
    "gun_img": "RockBall.png",
    "hp": 40,
    "armor": 6,
    "protection": 0,
    "speed": 0.8,
    "attack_cooldown": 2,
    "damage": 2,
    "attack_distance": 300,
}

ice_soul = {
    "name": "Ледяной дух",
    "img": "Ice spirit/walk-left/1.png",
    "gun_img": "Ice.png",
    "hp": 20,
    "armor": 6,
    "protection": 0,
    "speed": 1.2,
    "attack_cooldown": 2,
    "damage": 2,
    "attack_distance": 600,
}

fire_soul = {
    "name": "Огненный дух",
    "img": "Fire spirit/walk/1.png",
    "gun_img": "FireBall.png",
    "hp": 20,
    "armor": 6,
    "protection": 0,
    "speed": 1.2,
    "attack_cooldown": 2,
    "damage": 2,
    "attack_distance": 600,
}

dog = {
    "name": "Пёс",
    "img": "Dog/walk-left/1.png",
    "hp": 20,
    "armor": 0,
    "protection": 0,
    "speed": 2.5,
    "attack_cooldown": 1,
    "damage": 2,
    "attack_distance": 70,
}

tree = {
    "name": "Ёлка",
    "img": "Tree/StandUp/1.png",
    "hp": 10,
    "armor": 5,
    "protection": 0,
    "speed": 1.5,
    "damage": 1,
    "attack_cooldown": 5,
    "attack_distance": 100,
}

# BOSSES
dragonboss = {
    "name": "Древний Дракон",
    "img": "Dragon/Walk-right/1.png",
    "hp": 150,
    "armor": 0,
    "protection": 0,
    "speed": 1.5,
    "fly_speed": 5,
    "attack_cooldown": 3,
    "damage": 2,
    "attack_distance": 1000,
    "m_range": 100
}

necroboss = {
    "name": "Некромант",
    "img": "Necromancer/Walk-left/1.png",
    "hp": 100,
    "armor": 0,
    "protection": 0,
    "speed": 1.2,
    "attack_cooldown": 2,
    "damage": 3,
    "attack_distance": 500,
}

hunter = {
    "name": "Охотник",
    "img": "Hunter/walk-left/1.png",
    "hp": 80,
    "armor": 0,
    "protection": 0,
    "speed": 0.8,
    "attack_cooldown": 2,
    "damage": 3,
    "attack_distance": 1000,
}

golem = {
    "name": "Голем",
    "img": "Golem/walk-left/1.png",
    "hp": 150,
    "armor": 0,
    "protection": 1,
    "speed": 0.5,
    "attack_cooldown": 2,
    "damage": 3,
    "attack_distance": 600,
}
