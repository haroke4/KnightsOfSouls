"""
Вся инфа про боссов, персов
"""
import sqlite3


def increase_mob_characteristics(x):
    con = sqlite3.connect("files/db.sqlite")
    cur = con.cursor()
    for mob in [mini_golem, snake, ice_soul, fire_soul, dog, tree, dragonboss, necroboss, hunter, golem]:
        data = cur.execute(f"""SELECT * FROM mobs WHERE name = '{mob["name"]}'""").fetchone()
        mob["hp"] = data[1] * x
        mob["armor"] = data[2] * x
        mob["damage"] = data[3] * x


def make_default_mob_characteristics():
    con = sqlite3.connect("files/db.sqlite")
    cur = con.cursor()
    for mob in [mini_golem, snake, ice_soul, fire_soul, dog, tree, dragonboss, necroboss, hunter, golem]:
        data = cur.execute(f"""SELECT * FROM mobs WHERE name = '{mob["name"]}'""").fetchone()
        mob["hp"] = data[1]
        mob["armor"] = data[2]
        mob["damage"] = data[3]
    con.close()


# HEROES
spearman = {
    "name": "Копейщик",
    "img": "SpearMan/down/1.png",
    "gun_img": "arrow.png",
    "hp": 5,
    "armor": 5,
    "protection": 0,
    "walk_speed": 1.25,
    "run_speed": 2.5,
    "attack_cooldown": 1,
    "damage": 7,
}
magicman = {
    "name": "Ледяной колдун",
    "img": "MagicMan/down/1.png",
    "gun_img": "magicman_fire.png",
    "hp": 7,
    "armor": 7,
    "protection": 0,
    "walk_speed": 1.0,
    "run_speed": 2.0,
    "attack_cooldown": 2,
    "damage": 7,
    "description": "Создает ледяную токсину из земли, враги замедляются при попаданий",
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
    "damage": 8,
}

# ENEMY
snake = {
    "name": "Snake",
    "img": "Snake/walk-left/1.png",
    "hp": 1,
    "armor": 0,
    "protection": 0,
    "speed": 3,
    "attack_cooldown": 2,
    "damage": 1,
    "attack_distance": 90,
}

mini_golem = {
    "name": "Mini-golem",
    "img": "Mini-golem/walk-left/1.png",
    "gun_img": "RockBall.png",
    "hp": 12,
    "armor": 0,
    "protection": 0,
    "speed": 0.8,
    "attack_cooldown": 2,
    "damage": 2,
    "attack_distance": 300,
}

ice_soul = {
    "name": "Ice-soul",
    "img": "Ice spirit/walk-left/1.png",
    "gun_img": "Ice.png",
    "hp": 10,
    "armor": 0,
    "protection": 0,
    "speed": 1.2,
    "attack_cooldown": 2,
    "damage": 2,
    "attack_distance": 600,
}

fire_soul = {
    "name": "Fire-soul",
    "img": "Fire spirit/walk/1.png",
    "gun_img": "FireBall.png",
    "hp": 10,
    "armor": 0,
    "protection": 0,
    "speed": 1.2,
    "attack_cooldown": 2,
    "damage": 2,
    "attack_distance": 600,
}

dog = {
    "name": "Dog",
    "img": "Dog/walk-left/1.png",
    "hp": 15,
    "armor": 0,
    "protection": 0,
    "speed": 2.5,
    "attack_cooldown": 1,
    "damage": 2,
    "attack_distance": 70,
}

tree = {
    "name": "Tree",
    "img": "Tree/StandUp/1.png",
    "hp": 15,
    "armor": 0,
    "protection": 0,
    "speed": 1.5,
    "damage": 1,
    "attack_cooldown": 5,
    "attack_distance": 100,
}

# BOSSES
dragonboss = {
    "name": "Dragon",
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
    "name": "Necromancer",
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
    "name": "Hunter",
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
    "name": "Golem",
    "img": "Golem/walk-left/1.png",
    "hp": 150,
    "armor": 0,
    "protection": 1,
    "speed": 0.5,
    "attack_cooldown": 2,
    "damage": 3,
    "attack_distance": 600,
}
