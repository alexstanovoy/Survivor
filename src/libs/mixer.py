import libs.settings as settings

from pygame.mixer import Sound
from pygame.mixer import music
from random import choice


ALREADY_LOADED = {}
LAST_MUSIC = ''


def play_music():
    global LAST_MUSIC
    if LAST_MUSIC == '':
        LAST_MUSIC = choice(settings.MUSIC)
        music.queue(LAST_MUSIC)
    path = LAST_MUSIC
    while path is LAST_MUSIC:
        path = choice(settings.MUSIC)
    music.load(path)
    music.set_volume(0.15)
    music.play()


def play_sound(path):
    if path not in ALREADY_LOADED:
        ALREADY_LOADED[path] = Sound(path)
    ALREADY_LOADED[path].play()
