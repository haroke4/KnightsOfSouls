"""
Вся инфа про боссов, персов
"""


def increase_mob_characteristics(x: object) -> object:
    for i in [mini_golem, snake]:
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
    "attack_cooldown": 1,
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
    "speed": 2.5,
    "attack_cooldown": 2,
    "damage": 1,
    "attack_distance": 50,
}

mini_golem = {
    "name": "Мини-голем",
    "img": "Mini-golem/walk-left/1.png",
    "gun_img": "RockBall.png",
    "hp": 6,
    "armor": 6,
    "protection": 0,
    "speed": 0.8,
    "attack_cooldown": 2,
    "damage": 2,
    "attack_distance": 300,
}

dog = {
    "name": "Пёс",
    "img": "Mini-golem/walk-left/1.png",
    "hp": 10,
    "armor": 5,
    "protection": 0,
    "speed": 1.5,
    "attack_cooldown": 2,
    "damage": 1,
    "attack_distance": 100,
}

tree = {
    "name": "Ёлка",
    "img": "Mini-golem/walk-left/1.png",
    "hp": 10,
    "armor": 5,
    "protection": 0,
    "speed": 3,
    "damage": 1,
}

# BOSSES
dragonboss = {
    "name": "Древний Дракон",
    "img": "Mini-golem/walk-left/1.png",
    "hp": 30,
    "armor": 20,
    "protection": 0,
    "speed": 0.8,
    "fly_speed": 2,
    "attack_cooldown": 2,
    "damage": 2,
    "attack_distance": 800,
    "m_range": 150
}

necroboss = {
    "name": "Некромант",
    "img": "Mini-golem/walk-left/1.png",
    "hp": 30,
    "armor": 20,
    "protection": 0,
    "speed": 0.8,
    "fly_speed": 2,
    "attack_cooldown": 2,
    "damage": 2,
    "attack_distance": 800,
}
