import pygame, pygame.gfxdraw
from random import randint
from functions import *


class Ball:
    def __init__(self, scene=None, radius=10, coordinates=(0, 0), speed=(0, 0), color=(255, 255, 255)):
        self.scene = scene
        self.radius = radius
        self.color = color
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.vx = speed[0]
        self.vy = speed[1]
        self.elasticity = 0.5
        self.friction = 1
        self.volume = (4 / 3) * pi * radius ** 3
        self.density = 1e-5
        self.mass = self.volume * self.density

    def canvas_borders_collision(self):
        if self.y >= scene.height - self.radius:
            self.y += (scene.height - self.y) - self.radius
            self.vy *= -self.elasticity
            self.y += self.vy * scene.update_time
            self.vx *= self.friction
        elif self.y <= self.radius:
            self.y += self.radius - self.y
            self.vy *= -self.elasticity
            self.y += self.vy * scene.update_time
            self.vx *= self.friction

        if self.x >= scene.width - self.radius:
            self.x += (scene.width - self.x) - self.radius
            self.vx *= -self.elasticity
            self.x += self.vx * scene.update_time
            self.vy *= self.friction
        elif self.x <= self.radius:
            self.x += self.radius - self.x
            self.vx *= -self.elasticity
            self.x += self.vx * scene.update_time
            self.vy *= self.friction

    def update_coordinates(self):
        self.canvas_borders_collision()
        self.vy += scene.g * scene.update_time
        self.y += self.vy * scene.update_time
        self.x += self.vx * scene.update_time

    def draw(self):
        pygame.gfxdraw.aacircle(self.scene.window,
                                int(self.x), int(self.y), self.radius, self.color)
        pygame.gfxdraw.filled_circle(self.scene.window,
                                     int(self.x), int(self.y), self.radius, self.color)


class Scene:
    def __init__(self, objects: list):
        self.height = 768
        self.width = 1000
        self.fps_limit = 100
        self.tick_time = 100 / self.fps_limit
        self.update_time = 0.01
        self.bg_color = 'black'
        self.g = 0
        self.objects = objects
        for obj in self.objects:
            obj.scene = self
        self.G = 1

        pygame.init()
        self.window = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

        self.running = True

    def add_new_ball(self, event):
        colors = (
            (255, 255, 255),
            (255, 0, 0),
            (0, 255, 0),
            (0, 0, 255),
            (255, 255, 0),
            (255, 0, 255),
            (0, 255, 255)
        )
        radius = randint(30, 30)
        x = event.pos[0]
        y = event.pos[1]
        vx = randint(0, 0)
        vy = randint(0, 0)
        color = colors[randint(0, len(colors) - 1)]
        new_ball = Ball(self, radius=radius, coordinates=(x, y), speed=(vx, vy), color=color)
        self.objects.append(new_ball)

    def all_g_force(self, object_1):
        sum_ax = 0
        sum_ay = 0
        for object_2 in self.objects:
            if object_1 != object_2:
                ax, ay = calculate_gravitational_acceleration(self.G, object_1, object_2)
                sum_ax += ax
                sum_ay += ay

        return sum_ax, sum_ay

    def update_by_gravity(self, object_1):
        ax, ay = self.all_g_force(object_1)
        dvx = ax / self.update_time
        dvy = ay / self.update_time

        object_1.vx += dvx
        object_1.vy += dvy

        object_1.x += object_1.vx * self.update_time
        object_1.y += object_1.vy * self.update_time

    def collide(self, object_1, object_2):
        if is_collision(object_1, object_2):
            k = 0.1

            vx1 = object_1.vx
            vy1 = object_1.vy
            v1 = sqrt(vx1 ** 2 + vy1 ** 2)
            m1 = object_1.mass
            theta1 = atan2(vy1, vx1)

            vx2 = object_2.vx
            vy2 = object_2.vy
            v2 = sqrt(vx2 ** 2 + vy2 ** 2)
            m2 = object_2.mass
            theta2 = atan2(vy2, vx2)

            phi = atan2((object_2.y - object_1.y), (object_2.x - object_1.x))

            v1new = v1 - (1 + k) * (m2 / (m2 + m1)) * (v1 - v2)
            v2new = v2 + (1 + k) * (m1 / (m2 + m1)) * (v1 - v2)

            v1 = v1new
            v2 = v2new

            v1x_new = ((v1 * cos(theta1 - phi) * (m1 - m2) + 2 * m2 * v2 * cos(theta2 - phi)) / (m1 + m2)) * cos(
                phi) + v1 * sin(theta1 - phi) * cos(phi + pi / 2)
            v1y_new = ((v1 * cos(theta1 - phi) * (m1 - m2) + 2 * m2 * v2 * cos(theta2 - phi)) / (m1 + m2)) * sin(
                phi) + v1 * sin(theta1 - phi) * sin(phi + pi / 2)

            v2x_new = ((v2 * cos(theta2 - phi) * (m2 - m1) + 2 * m1 * v1 * cos(theta1 - phi)) / (m1 + m2)) * cos(
                phi) + v2 * sin(theta2 - phi) * cos(phi + pi / 2)
            v2y_new = ((v2 * cos(theta2 - phi) * (m2 - m1) + 2 * m1 * v1 * cos(theta1 - phi)) / (m1 + m2)) * sin(
                phi) + v2 * sin(theta2 - phi) * sin(phi + pi / 2)

            object_1.vx, object_1.vy = v1x_new, v1y_new
            object_2.vx, object_2.vy = v2x_new, v2y_new

            object_1.x += object_1.vx * self.update_time
            object_1.y += object_1.vy * self.update_time
            object_2.x += object_2.vx * self.update_time
            object_2.y += object_2.vy * self.update_time

    def collisions_manager(self):
        collisions = []

        for obj1 in self.objects:
            for obj2 in self.objects:
                if obj1 != obj2:
                    collisions.append(is_collision(obj1, obj2))
                    self.collide(obj1, obj2)

        if any(collisions):
            for object_1 in self.objects:
                for object_2 in self.objects:
                    displace_by_intersection(object_1, object_2)

    def update_frame(self):
        self.collisions_manager()
        for object_1 in self.objects:
            object_1.update_coordinates()
            self.update_by_gravity(object_1)
            object_1.draw()

    def update_ui(self):
        self.window.fill(self.bg_color)
        self.update_frame()
        pygame.display.flip()

    def tick(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.add_new_ball(event)
            elif event.type == pygame.QUIT:
                self.running = False

    def next_frame(self):
        self.tick()
        self.clock.tick(60)
        self.update_ui()

    def loop(self):
        while self.running:
            self.next_frame()
        pygame.quit()


sun = Ball(scene=None, radius=5, coordinates=(500, 500), speed=(0, 0), color=(255, 255, 0))
sun.mass = 1000
comet = Ball(scene=None, radius=1, coordinates=(500, 100), speed=(30, 0), color=(255, 255, 255))
objects = [sun, comet]

if __name__ == '__main__':
    scene = Scene(objects=objects)

    scene.loop()
