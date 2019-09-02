import libs.settings as settings

from time import sleep
from libs.maths import get_origin, pic_angle, pic_corner
from pygame.surface import Surface
from pygame import SRCALPHA, BLEND_RGBA_SUB
from pygame.display import update
from pygame.draw import rect
from pygame.font import Font
from pygame.event import get as get_events
from pygame.transform import rotate

from numpy import array as vector


ENTITY_ANIM_STATE = dict()


def display_preparation():
    settings.SCENE.blit(settings.SPRITE['background'], (0, 0))
    settings.GUI = Surface(
                        (settings.GUI_X, settings.GUI_Y),
                        SRCALPHA,
                        32
                    ).convert_alpha()
    settings.DISPLAY_FILTER = Surface((settings.WIDTH,
                                       settings.HEIGHT))
    settings.DISPLAY_FILTER.fill(settings.DISPLAY_FILTER_COLOR)


def display_render():
    settings.SCENE.blit(settings.DISPLAY_FILTER,
                        settings.DISPLAY,
                        special_flags=BLEND_RGBA_SUB)
    settings.SCENE.blit(settings.GUI, (0, settings.HEIGHT - settings.GUI_Y))
    update()


def single_color_bar(color, x, y, w, h, thickness, value, maxvalue):
    rect(settings.GUI, color, [x, y, w * value / maxvalue, h])
    rect(settings.GUI, color, [x, y, w, h], thickness)


def text_info(text, x, y, size, antialazing, color):
    info = Font(None, size).render(text, True, color)
    settings.GUI.blit(info, [x, y])


def game_over():
    settings.SCENE.fill((255, 255, 255))

    text = Font(None, 120).render(
        'Game Over. Score: ' +
        str(settings.SCORE),
        True,
        (0, 0, 0)
    )
    text_rect = text.get_rect()
    settings.SCENE.blit(text, [settings.WIDTH // 2 - text_rect.width // 2,
                               settings.HEIGHT // 2 - text_rect.height // 2])
    update()
    sleep(1.5)

    text = Font(None, 80).render(
        'Press any key...',
        True,
        (0, 0, 0)
    )
    text_rect = text.get_rect()
    settings.SCENE.blit(text, [settings.WIDTH // 2 - text_rect.width // 2,
                               settings.HEIGHT // 2 - text_rect.height // 2 + 70])
    update()

    for event in get_events():
        pass

    while True:
        for event in get_events():
            if event.type == settings.QUIT:
                exit(0)
            elif event.type == settings.KEYDOWN:
                exit(0)
            elif event.type == settings.MOUSEBUTTONDOWN:
                exit(0)
        settings.CLOCK.tick(settings.FPS)


def add_filter(mask, pos):
    settings.DISPLAY_FILTER.blit(mask, tuple(pos))


def add_rotated_filter(sprite, point, shift, angle):
    add_filter(
        rotate(sprite, angle),
        get_origin(
            sprite.get_size(),
            point,
            shift,
            angle
        )
    )


def draw_pic(sprite, center, direction):
    pic = rotate(sprite, pic_angle(direction))
    settings.SCENE.blit(
        pic,
        pic_corner(
            center,
            vector(pic.get_size())
        )
    )


def draw_entity(entity):
    num = ENTITY_ANIM_STATE.get(entity, 0)
    draw_pic(entity.sprite[num],
             entity.center,
             entity.direction)
    ENTITY_ANIM_STATE[entity] = (num+1) % len(entity.sprite)
