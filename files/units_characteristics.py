"""
Вся инфа про боссов, персов
"""
# HEROES
spearman = {
    "name": "Копейщик",
    "img": "abobus.png",
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
    "img": "abobus.png",
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
    "img": "abobus.png",
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
goblin = {
    "name": "Маленький гоблин",
    "img": "abobus.png",
    "hp": 1,
    "armor": 0,
    "run_speed": 2.5,
    "attack_cooldown": 2.5,
    "damage": 2,
}



