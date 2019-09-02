import numpy as np
from pygame.math import Vector2
from numpy import array as vector


def norm(vec):
    length = np.linalg.norm(vec)
    return vec / length if length != 0 else vector([0, 0])


def vec_rotate(vec, angle):
    return vector([vec[0]*np.cos(angle)-vec[1]*np.sin(angle),
                   vec[0]*np.sin(angle)+vec[1]*np.cos(angle)])


def angle(vec1, vec2):
    vec1_u = norm(vec1)
    vec2_u = norm(vec2)
    return np.arccos(np.clip(np.dot(vec1_u, vec2_u), -1.0, 1.0))


def pic_angle(vec):
    if vec[0] <= 0:
        return np.rad2deg(np.arccos(np.dot(vec, vector([0, -1]))))
    else:
        return 180.0 + np.rad2deg(np.arccos(np.dot(-vec, vector([0, -1]))))


def pic_corner(center, size=vector([0, 0])):
    return center - size // 2


def distance(vec1, vec2):
    return np.sqrt(np.sum((vec1 - vec2)**2))


def point_over_basis(vec1, vec2, direction):
    temp = vector([direction[0]*vec2[0]-direction[1]*vec2[1],
                   direction[1]*vec2[0]+direction[0]*vec2[1]])
    return (vec1 + temp).astype(int)


def get_origin(size, pos, origin_pos, angle):
    w, h = size[0], size[1]
    box_rotate = [p.rotate(angle) for p in
                  [Vector2(p) for p in
                   [(0, 0), (w, 0), (w, -h), (0, -h)]]]
    pivot = Vector2(origin_pos[0], -origin_pos[1])
    pivot_move = pivot.rotate(angle) - pivot

    return (pos[0] - origin_pos[0] +
            min(box_rotate, key=lambda p: p[0])[0] - pivot_move[0],
            pos[1] - origin_pos[1] -
            max(box_rotate, key=lambda p: p[1])[1] + pivot_move[1])
