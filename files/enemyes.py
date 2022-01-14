from global_stuff import *
from heroes import *


class BaseEnemy(BaseGameObject):
    def __init__(self, x, y, image, hp, armor, run_speed, attack_cooldown, damage):
        self.is_active = False
        self.dead = False
        self.max_hp = self.hp = hp
        self.max_armor = self.armor = armor
        self.initial_run_speed = self.run_speed = run_speed
        self.attack_cooldown = attack_cooldown
        self.damage = damage
        self.velocity = pygame.Vector2(0, 0)
        super().__init__(x, y, image, [6, 35, 36, 15], ENEMY_TEAM)

    def take_damage(self, damage):
        if damage > 0:
            self.armor -= damage
            if self.armor < 0:
                self.hp -= abs(self.armor)
                if self.hp <= 0:
                    self.die()
                self.armor = 0


class GoblinEnemy(BaseEnemy):
    def __init__(self, x=0, y=0):
        data = units_characteristics.goblin
        super().__init__(x, y, data["img"], data["hp"], data["armor"], data["run_speed"],
                         data["attack_cooldown"], data["damage"])
