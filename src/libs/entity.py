from pygame import Rect
from pygame.sprite import Sprite

from libs.maths import pic_corner

from numpy import array as vector


class Entity(Sprite):

    def __init__(self,
                 center=vector([0, 0]),
                 direction=vector([0, 0]),
                 size=vector([0, 0]),
                 ability_lst=list(),
                 draw_func=None,
                 sprite=None,
                 score=None):
        Sprite.__init__(self)
        self.center = center
        self.ability = ability_lst
        self.size = size
        self.draw_func = draw_func
        self.direction = direction
        self.sprite = sprite
        self.update_rect()
        self.score = score

    def update_rect(self):
        self.rect = Rect(*pic_corner(self.center, self.size),
                         *self.size)

    def add_ability(self, *ability_lst):
        self.ability.append(list(ability_lst))

    def del_ability(self, ability):
        for self_ability in self.ability:
            if isinstance(self_ability, ability):
                self.ability.remove(self_ability)

    def get_ability(self, ability):
        for self_ability in self.ability:
            if isinstance(self_ability, ability):
                return self_ability
        return None

    def update(self):
        self.update_rect()
        for ability in self.ability:
            ability.update(self)
        if self.draw_func is not None:
            self.draw_func(self)
