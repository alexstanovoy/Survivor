#!/usr/bin/python3
import libs.mixer as mixer
import libs.factory as factory
import libs.settings as settings

from pygame import init
from pygame.display import set_mode
from pygame.time import set_timer, Clock
from pygame.event import get as get_events
from pygame.mouse import get_pos

from libs.moving import resolve_moving_key_up, resolve_moving_key_down
from libs.moving import resolve_mouse_key_down
from libs.render import display_preparation, display_render, \
                        single_color_bar, text_info, game_over
from libs.ability import Health, Armor
from libs.functions import update_direction

from numpy import array as vector


init()
settings.SCENE = set_mode(settings.DISPLAY, settings.MODE)
settings.WIDTH, settings.HEIGHT = settings.SCENE.get_rect()[2:]
settings.CLOCK = Clock()
settings.GLOBAL_PLAYERS['player0'] = factory.Player(settings.WIDTH // 2,
                                                    settings.HEIGHT // 2)


mixer.play_music()
set_timer(settings.CREATE_ENEMY_EVENT, settings.MONSTER_FREQ)
set_timer(settings.SCORE_DOWN, settings.SCORE_DOWN_FREQ)


def game_event_resolve(event):
    if event.type == settings.QUIT:
        exit(0)
    elif event.type == settings.KEYUP:
        if event.key in settings.KEY_MOVING:
            resolve_moving_key_up(settings.GLOBAL_PLAYERS['player0'],
                                  event)
    elif event.type == settings.KEYDOWN:
        if event.key in settings.KEY_MOVING:
            resolve_moving_key_down(settings.GLOBAL_PLAYERS['player0'],
                                    event)
    elif event.type == settings.MOUSEBUTTONDOWN:
        if event.button in settings.MOUSE_BUTTONS:
            resolve_mouse_key_down(settings.GLOBAL_PLAYERS['player0'],
                                   event)
    elif event.type == settings.CREATE_ENEMY_EVENT:
        settings.add_global_event(
            factory.spawn_in_edge,
            factory.random_enemy(settings.GLOBAL_PLAYERS['player0'])
        )
    elif event.type == settings.SCORE_DOWN:
        settings.SCORE -= settings.SCORE_DOWN_VAL
        settings.SCORE = max(settings.SCORE, 0)


while True:

    display_preparation()

    for event in get_events():
        game_event_resolve(event)

    if settings.GLOBAL_PLAYERS['player0'].get_ability(Health).health <= 0:
        game_over()

    settings.add_global_event(update_direction,
                              settings.GLOBAL_PLAYERS['player0'],
                              vector(get_pos()))
    settings.add_global_event(
        single_color_bar,
        *settings.GUI_HEALTH_PARAMS,
        settings.GLOBAL_PLAYERS['player0'].get_ability(Health).health,
        settings.GLOBAL_PLAYERS['player0'].get_ability(Health).max_health
    )
    settings.add_global_event(
        single_color_bar,
        *settings.GUI_ARMOR_PARAMS,
        settings.GLOBAL_PLAYERS['player0'].get_ability(Armor).armor,
        settings.GLOBAL_PLAYERS['player0'].get_ability(Armor).max_armor
    )
    settings.add_global_event(
        text_info,
        'Score: ' + str(settings.SCORE),
        *settings.GUI_SCORE_PARAMS
    )

    settings.resolve_updates()
    settings.resolve_events()

    display_render()
