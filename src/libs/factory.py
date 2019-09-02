import libs.settings as settings

from random import randint
from libs.ability import Health, Armor, Movement, PistolGlock, \
                         Collision, AutoKill, Flashlight, AIMeleeAttack, \
                         AIForwardMovement, Glow
from libs.entity import Entity
from libs.render import draw_entity
from libs.functions import deal_linear_armor_health_damage

from numpy import array as vector


def Player(x, y):
    return Entity(
                ability_lst=[Health(
                                health=settings.PLAYER_MAX_HEALTH,
                                max_health=settings.PLAYER_MAX_HEALTH
                             ),
                             Armor(
                                armor=settings.PLAYER_MAX_ARMOR,
                                max_armor=settings.PLAYER_MAX_ARMOR
                             ),
                             Movement(
                                speed=vector([
                                    settings.PLAYER_SPEED,
                                    settings.PLAYER_SPEED
                                    ]),
                                speed_mlp=vector([0, 0])),
                             PistolGlock(),
                             Collision(),
                             AutoKill(
                                -settings.AUTOKILL_RANGE,
                                -settings.AUTOKILL_RANGE,
                                settings.AUTOKILL_RANGE,
                                settings.AUTOKILL_RANGE
                             ),
                             Flashlight(
                                sprite=settings.SPRITE['flashlight'],
                                point=settings.PLAYER_HANDPOS
                             )],
                center=vector([x, y]),
                size=vector([settings.PLAYER_SIZE,
                             settings.PLAYER_SIZE]),
                draw_func=draw_entity,
                sprite=settings.SPRITE['player']
        )


def Zombie1(x, y, target):
    return Entity(
                ability_lst=[Health(
                                health=settings.ZOMBIE1_MAX_HEALTH,
                                max_health=settings.ZOMBIE1_MAX_HEALTH
                             ),
                             AIForwardMovement(
                                target=target,
                                speed=settings.ZOMBIE1_SPEED,
                                limit=settings.ZOMBIE1_ATTACK_DISTANCE
                             ),
                             AIMeleeAttack(
                                target=target,
                                distance=settings.ZOMBIE1_ATTACK_DISTANCE,
                                damage=settings.ZOMBIE1_DAMAGE,
                                func=deal_linear_armor_health_damage
                             ),
                             Collision()],
                center=vector([x, y]),
                size=vector([settings.ZOMBIE1_SIZE,
                             settings.ZOMBIE1_SIZE]),
                draw_func=draw_entity,
                sprite=settings.SPRITE['zombie1'],
                score=settings.ZOMBIE1_SCORE
        )


def Zombie2(x, y, target):
    return Entity(
                ability_lst=[Health(
                                health=settings.ZOMBIE2_MAX_HEALTH,
                                max_health=settings.ZOMBIE2_MAX_HEALTH
                             ),
                             AIForwardMovement(
                                target=target,
                                speed=settings.ZOMBIE2_SPEED,
                                limit=settings.ZOMBIE2_ATTACK_DISTANCE
                             ),
                             AIMeleeAttack(
                                target=target,
                                distance=settings.ZOMBIE2_ATTACK_DISTANCE,
                                damage=settings.ZOMBIE2_DAMAGE,
                                func=deal_linear_armor_health_damage
                             ),
                             Collision()],
                center=vector([x, y]),
                size=vector([settings.ZOMBIE2_SIZE,
                             settings.ZOMBIE2_SIZE]),
                draw_func=draw_entity,
                sprite=settings.SPRITE['zombie2'],
                score=settings.ZOMBIE2_SCORE
        )


def Zombie3(x, y, target):
    return Entity(
                ability_lst=[Health(
                                health=settings.ZOMBIE3_MAX_HEALTH,
                                max_health=settings.ZOMBIE3_MAX_HEALTH),
                             AIForwardMovement(
                                target=target,
                                speed=settings.ZOMBIE3_SPEED,
                                limit=settings.ZOMBIE3_ATTACK_DISTANCE),
                             AIMeleeAttack(
                                target=target,
                                distance=settings.ZOMBIE3_ATTACK_DISTANCE,
                                damage=settings.ZOMBIE3_DAMAGE,
                                func=deal_linear_armor_health_damage
                             ),
                             Collision()],
                center=vector([x, y]),
                size=vector([settings.ZOMBIE2_SIZE,
                             settings.ZOMBIE2_SIZE]),
                draw_func=draw_entity,
                sprite=settings.SPRITE['zombie3'],
                score=settings.ZOMBIE2_SCORE
        )


def Demon(x, y, target):
    return Entity(
                ability_lst=[Health(
                                health=settings.DEMON_MAX_HEALTH,
                                max_health=settings.DEMON_MAX_HEALTH
                             ),
                             AIForwardMovement(
                                target=target,
                                speed=settings.DEMON_SPEED,
                                limit=settings.DEMON_ATTACK_DISTANCE
                             ),
                             AIMeleeAttack(
                                target=target,
                                distance=settings.DEMON_ATTACK_DISTANCE,
                                damage=settings.DEMON_DAMAGE,
                                func=deal_linear_armor_health_damage),
                             Collision(),
                             Glow(sprite=settings.SPRITE['glowcircle'])],
                center=vector([x, y]),
                size=vector([settings.DEMON_SIZE,
                             settings.DEMON_SIZE]),
                draw_func=draw_entity,
                sprite=settings.SPRITE['demon'],
                score=settings.DEMON_SCORE)


ALL_EMEMIES = [Zombie1, Zombie2, Zombie3, Demon]


def random_enemy(target):
    num, sm = randint(1, settings.CHANCES_SUM), 0
    for i in range(len(settings.ENEMY_CHANCES)):
        sm += settings.ENEMY_CHANCES[i]
        if sm >= num:
            return ALL_EMEMIES[i](0, 0, target)


def spawn_in_edge(entity):
    def choose_intervals(a, b, c, d):
        if randint(0, 1):
            return randint(a, b)
        else:
            return randint(c, d)
    entity.center = vector([
                        choose_intervals(
                            -settings.MAX_RANGE,
                            -settings.MIN_RANGE,
                            settings.WIDTH+settings.MIN_RANGE,
                            settings.WIDTH+settings.MAX_RANGE
                        ),
                        choose_intervals(
                            -settings.MAX_RANGE,
                            -settings.MIN_RANGE,
                            settings.HEIGHT+settings.MIN_RANGE,
                            settings.HEIGHT+settings.MAX_RANGE
                        )])
    settings.add_enemy(entity)
