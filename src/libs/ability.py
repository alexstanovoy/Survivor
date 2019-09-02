import libs.settings as settings

from libs.maths import distance, norm, point_over_basis, \
                       pic_angle, pic_corner
from libs.render import add_rotated_filter, add_filter

from pygame.sprite import spritecollideany
from pygame.transform import rotate

from numpy import array as vector


class Ability:
    pass


class Movement(Ability):

    def __init__(self, speed, speed_mlp):
        self.speed = speed
        self.speed_mlp = speed_mlp

    def update(self, entity):
        entity.center += (self.speed * self.speed_mlp).astype(int)


class AIForwardMovement(Ability):

    def __init__(self, target, speed, limit):
        self.speed = speed
        self.target = target
        self.limit = limit

    def update(self, entity):
        if distance(entity.center, self.target.center) > self.limit:
            entity.direction = norm(self.target.center - entity.center)
            entity.center += (self.speed * entity.direction).astype(int)


class AIMeleeAttack(Ability):

    def __init__(self, target, distance, damage, func):
        self.target = target
        self.distance = distance
        self.damage = damage
        self.func = func

    def update(self, entity):
        if distance(entity.center, self.target.center) <= self.distance:
            settings.add_global_event(self.func,
                                      self.target,
                                      self.damage)


class Health(Ability):

    def __init__(self, health, max_health):
        self.health = health
        self.max_health = max_health

    def update(self, entity):
        pass


class Armor(Ability):

    def __init__(self, armor, max_armor):
        self.armor = armor
        self.max_armor = max_armor

    def update(self, entity):
        pass


class AutoDelete(Ability):

    def __init__(self, deadx1, deady1, deadx2, deady2):
        self.deadx1 = deadx1
        self.deady1 = deady1
        self.deadx2 = deadx2
        self.deady2 = deady2

    def update(self, entity):
        if not (self.deadx1 <= entity.center[0] <= self.deadx2 and
                self.deady1 <= entity.center[1] <= self.deady2):
            entity.kill()


class PistolGlock(Ability):

    def __init__(self):
        pass

    def update(self, entity):
        pass


class Collision(Ability):

    def __init__(self, coll_func=None, groups=[]):
        self.coll_func = coll_func
        self.groups = groups

    def update(self, entity):
        if self.coll_func is not None and self.groups is not []:
            for group in self.groups:
                if not entity.alive():
                    break
                collision = spritecollideany(entity, group)
                if collision is not None:
                    self.coll_func(entity, collision)


class Flashlight(Ability):

    def __init__(self, sprite, point):
        self.sprite = sprite
        self.point = point

    def update(self, entity):
        settings.add_global_event(add_rotated_filter,
                                  self.sprite,
                                  point_over_basis(entity.center,
                                                   self.point,
                                                   entity.direction),
                                  (self.sprite.get_size()[0] // 2,
                                   self.sprite.get_size()[1]),
                                  pic_angle(entity.direction))


class Glow(Ability):

    def __init__(self, sprite):
        self.sprite = sprite

    def update(self, entity):
        pic = rotate(self.sprite, pic_angle(entity.direction))
        settings.add_global_event(
            add_filter,
            pic,
            pic_corner(
                entity.center,
                vector(pic.get_size())
            )
        )


class AutoKill(Ability):

    def __init__(self, deadx1, deady1, deadx2, deady2):
        self.deadx1 = deadx1
        self.deady1 = deady1
        self.deadx2 = deadx2
        self.deady2 = deady2

    def update(self, entity):
        if not (self.deadx1 <= entity.center[0] <= self.deadx2 and
                self.deady1 <= entity.center[1] <= self.deady2):
            entity.get_ability(Health).health = 0
