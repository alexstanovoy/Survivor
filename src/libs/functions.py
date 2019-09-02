import libs.mixer as mixer
import libs.settings as settings

from libs.maths import point_over_basis, pic_angle, norm
from libs.render import draw_entity, add_rotated_filter
from libs.ability import Armor, Health, Movement, PistolGlock, \
                         AutoDelete, Collision
from libs.entity import Entity

from numpy import array as vector


def deal_linear_armor_damage(entity, amount):
    arm = entity.get_ability(Armor)
    if arm is not None:
        arm.armor -= amount
        if arm.armor < 0:
            amount, arm.armor = -arm.armor, 0
        else:
            amount = 0
    return amount


def deal_linear_health_damage(entity, amount):
    hlh = entity.get_ability(Health)
    if hlh is not None:
        hlh.health -= amount
        if hlh.health <= 0:
            if entity.score is not None:
                settings.SCORE += entity.score
            entity.kill()
        else:
            amount = 0
    return amount


def deal_linear_armor_health_damage(entity, amount):
    amount = deal_linear_health_damage(entity,
                                       deal_linear_armor_damage(entity,
                                                                amount))
    return amount


def movement_mlp(entity, speed_mlp):
    mvm = entity.get_ability(Movement)
    mvm.speed_mlp += speed_mlp


def movement_spd(entity, speed):
    mvm = entity.get_ability(Movement)
    mvm.speed = speed


def update_direction(entity, by_point):
    entity.direction = norm(by_point - entity.center)


def pistolglock_shoot(entity):
    if entity.get_ability(PistolGlock) is not None and \
       entity.direction[0] != 0 and entity.direction[1] != 0:
        mixer.play_sound(settings.SOUND['glock'])
        pic = settings.SPRITE['glockshot']
        settings.add_global_event(add_rotated_filter,
                                  pic,
                                  point_over_basis(entity.center,
                                                   (0, 0),
                                                   entity.direction),
                                  (settings.SHIFT_BLOW_X,
                                   settings.SHIFT_BLOW_Y),
                                  pic_angle(entity.direction))
        settings.GLOBAL_SHOT.add(
            Entity(
                ability_lst=[Movement(
                                speed=vector([settings.GLOCK_SPEED,
                                              settings.GLOCK_SPEED]),
                                speed_mlp=entity.direction
                             ),
                             AutoDelete(
                                -settings.AUTOKILL_RANGE,
                                -settings.AUTOKILL_RANGE,
                                settings.AUTOKILL_RANGE,
                                settings.AUTOKILL_RANGE
                             ),
                             Collision(
                                coll_func=pistolglock_bullet_collision,
                                groups=[settings.GLOBAL_ENEMIES]
                             )],
                center=vector(point_over_basis(
                                entity.center,
                                settings.PLAYER_HANDPOS,
                                entity.direction
                             )),
                size=vector([settings.BULLET_SIZE_X,
                             settings.BULLET_SIZE_Y]),
                direction=entity.direction,
                draw_func=draw_entity,
                sprite=settings.SPRITE['glockbullet']
            )
        )


def pistolglock_bullet_collision(bullet, entity):
    deal_linear_armor_health_damage(entity, settings.GLOCK_DAMAGE)
    bullet.kill()
