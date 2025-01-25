from math import atan2, cos, sin, sqrt, pi


def calculate_gravitational_acceleration(G, object_1, object_2):

    x1 = object_1.x
    y1 = object_1.y
    x2 = object_2.x
    y2 = object_2.y
    m2 = object_2.mass

    phi = atan2(y2 - y1, x2 - x1)
    r_2 = (x2 - x1) ** 2 + (y2 - y1) ** 2
    a = (G * m2) / r_2
    ax = a * cos(phi)
    ay = a * sin(phi)

    return ax, ay


def calculate_collision_depth(object_1, object_2):
    centers_squared_distance = (object_2.x - object_1.x) ** 2 + (object_2.y - object_1.y) ** 2

    if centers_squared_distance < (object_2.radius + object_1.radius)**2:
        phi = atan2(object_2.y - object_1.y, object_2.x - object_1.x)
        distance = sqrt(centers_squared_distance)  # calculate distance from squared distance

        depth = object_2.radius + object_1.radius - distance

        depth_x = depth * cos(phi)
        depth_y = depth * sin(phi)

        move_1x = depth_x / 2
        move_1y = depth_y / 2
        move_2x = move_1x
        move_2y = move_1y
    else:
        move_1x, move_1y, move_2x, move_2y = 0, 0, 0, 0

    return -move_1x, -move_1y, move_2x, move_2y


def displace_by_intersection(object_1, object_2):
    if object_1 != object_2:
        move_1x, move_1y, move_2x, move_2y = calculate_collision_depth(object_1, object_2)
        object_1.x += move_1x
        object_1.y += move_1y
        object_2.x += move_2x
        object_2.y += move_2y


def is_collision(object_1, object_2):

    l_2 = (object_2.x - object_1.x) ** 2 + (object_2.y - object_1.y) ** 2

    return object_1 != object_2 and l_2 <= (object_2.radius + object_1.radius) ** 2
