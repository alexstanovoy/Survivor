from pygame import USEREVENT
from pygame.image import load
from pygame.sprite import Group
from pygame.transform import smoothscale

from pygame.locals import FULLSCREEN, K_w, K_s, K_a, K_d, \
                          QUIT, KEYUP, KEYDOWN, \
                          MOUSEBUTTONUP, MOUSEBUTTONDOWN


SCENE, CLOCK = None, None
WIDTH, HEIGHT = None, None
GLOBAL_PLAYERS = dict()
GLOBAL_ENEMIES = Group([])
GLOBAL_SHOT = Group([])
GLOBAL_EVENTS = []
DISPLAY = (0, 0)
MODE = FULLSCREEN
NEXT_ENTITY_NAME = 0
FPS = 60
MAX_ENEMY_COUNTER = 30
SCORE = 0

DISPLAY_FILTER = None
DISPLAY_FILTER_COLOR = (200, 200, 200)

GUI_X = 400
GUI_Y = 400
GUI = None
GUI_HEALTH_PARAMS = ((255, 0, 0), 5, GUI_X-50, 170, 20, 2)
GUI_ARMOR_PARAMS = ((128, 128, 128), 5, GUI_X-25, 170, 20, 2)
GUI_SCORE_PARAMS = (5, GUI_X-90, 50, True, (180, 180, 180))

KEY_UP, KEY_DOWN = K_w, K_s
KEY_LEFT, KEY_RIGHT = K_a, K_d
KEY_MOVING = set([KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT])

SHOOT = 1
MOUSE_BUTTONS = set([1])

PLAYER_MAX_HEALTH = 100
PLAYER_MAX_ARMOR = 200
PLAYER_SPEED = 10
PLAYER_SIZE = 60
PLAYER_HANDPOS = (35, 10)

ENEMY_CHANCES = [20, 13, 5, 1]
CHANCES_SUM = sum(ENEMY_CHANCES)

AUTOKILL_RANGE = 2000
MIN_RANGE = 300
MAX_RANGE = 500

ZOMBIE1_MAX_HEALTH = 100
ZOMBIE1_ATTACK_DISTANCE = 20
ZOMBIE1_DAMAGE = 10
ZOMBIE1_SPEED = 6
ZOMBIE1_SIZE = 60
ZOMBIE1_SCORE = 2

ZOMBIE2_MAX_HEALTH = 60
ZOMBIE2_ATTACK_DISTANCE = 20
ZOMBIE2_DAMAGE = 3
ZOMBIE2_SPEED = 13
ZOMBIE2_SIZE = 60
ZOMBIE2_SCORE = 4

ZOMBIE3_MAX_HEALTH = 200
ZOMBIE3_ATTACK_DISTANCE = 30
ZOMBIE3_DAMAGE = 7
ZOMBIE3_SPEED = 7
ZOMBIE3_SIZE = 80
ZOMBIE3_SCORE = 2

DEMON_MAX_HEALTH = 700
DEMON_ATTACK_DISTANCE = 60
DEMON_DAMAGE = 15
DEMON_SPEED = 4
DEMON_SIZE = 100
DEMON_SCORE = 15

BULLET_SIZE_X = 6
BULLET_SIZE_Y = 10

FLASHLIGHT_X = 500
FLASHLIGHT_Y = 800

SHIFT_BLOW_X = 150
SHIFT_BLOW_Y = 220

GLOWCIRCLE_SIZE = 200

SPRITE = {'player': [smoothscale(
                        load('resources/sprites/player/player.png'),
                        [PLAYER_SIZE,
                         PLAYER_SIZE]
                     )],
          'zombie1': [smoothscale(
                        load('resources/sprites/zombie1/'+str(i)+'.png'),
                        [ZOMBIE1_SIZE,
                         ZOMBIE1_SIZE]
                      ) for i in range(16)],
          'zombie2': [smoothscale(
                        load('resources/sprites/zombie2/'+str(i)+'.png'),
                        [ZOMBIE2_SIZE,
                         ZOMBIE2_SIZE]
                      ) for i in range(3)],
          'zombie3': [load(
                        'resources/sprites/zombie3/'+str(i)+'.png'
                      ) for i in range(32)],
          'demon': [smoothscale(
                        load('resources/sprites/demon/demon.png'),
                        [DEMON_SIZE,
                         DEMON_SIZE]
                    )],
          'glockbullet': [smoothscale(
                            load('resources/sprites/bullets/bullet.png'),
                            [BULLET_SIZE_X,
                             BULLET_SIZE_Y]
                          )],
          'background': load('resources/sprites/background.jpg'),
          'flashlight': smoothscale(
                            load('resources/sprites/mask/flashlight.png'),
                            [FLASHLIGHT_X,
                             FLASHLIGHT_Y]
                        ),
          'glowcircle': smoothscale(
                            load('resources/sprites/mask/glowcircle.png'),
                            [GLOWCIRCLE_SIZE,
                             GLOWCIRCLE_SIZE]
                        ),
          'glockshot': load('resources/sprites/mask/glockshot.png')}

MUSIC = ['resources/music/main1.ogg',
         'resources/music/main2.ogg',
         'resources/music/main3.ogg']
SOUND = {'glock': 'resources/sound/glock.ogg'}

MONSTER_FREQ = 1000
CREATE_ENEMY_EVENT = USEREVENT + 1

SCORE_DOWN = USEREVENT + 2
SCORE_DOWN_FREQ = 10000
SCORE_DOWN_VAL = 5

GLOCK_SPEED = 50
GLOCK_DAMAGE = 20


def add_enemy(entity):
    if len(GLOBAL_ENEMIES) < MAX_ENEMY_COUNTER:
        GLOBAL_ENEMIES.add(entity)


def add_global_event(event, *args):
    if event not in GLOBAL_EVENTS:
        GLOBAL_EVENTS.append((event, args))


def resolve_updates():
    for entity in GLOBAL_PLAYERS.values():
        entity.update()
    GLOBAL_ENEMIES.update()
    GLOBAL_SHOT.update()


def resolve_events():
    for event in GLOBAL_EVENTS:
        event[0](*event[1])
    GLOBAL_EVENTS.clear()
