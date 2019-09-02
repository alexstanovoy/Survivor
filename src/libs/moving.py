import libs.settings as settings
from libs.functions import movement_mlp, pistolglock_shoot


def resolve_moving_key_up(entity, event):
    if event.key == settings.KEY_LEFT:
        settings.add_global_event(movement_mlp, entity, (1, 0))
    elif event.key == settings.KEY_RIGHT:
        settings.add_global_event(movement_mlp, entity, (-1, 0))
    elif event.key == settings.KEY_UP:
        settings.add_global_event(movement_mlp, entity, (0, 1))
    elif event.key == settings.KEY_DOWN:
        settings.add_global_event(movement_mlp, entity, (0, -1))


def resolve_moving_key_down(entity, event):
    if event.key == settings.KEY_LEFT:
        settings.add_global_event(movement_mlp, entity, (-1, 0))
    elif event.key == settings.KEY_RIGHT:
        settings.add_global_event(movement_mlp, entity, (1, 0))
    elif event.key == settings.KEY_UP:
        settings.add_global_event(movement_mlp, entity, (0, -1))
    elif event.key == settings.KEY_DOWN:
        settings.add_global_event(movement_mlp, entity, (0, 1))


def resolve_mouse_key_down(entity, event):
    if event.button == settings.SHOOT:
        settings.add_global_event(pistolglock_shoot, entity)
