from tkinter import Tk, Canvas
from random import randint
from math import atan2, cos, sin, sqrt, pi

class Ball:
    def __init__(self, canvas, radius, coordinates, speed=(0, 0), color='white', mass=4e-4):
        self.canvas = canvas
        self.radius = radius
        self.color = color
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.vx = speed[0]
        self.vy = speed[1]
        self.elasticity = 0.5
        self.friction = 1
        self.volume = (4/3) * pi * radius ** 3
        self.density = 1e-5
        self.mass = self.volume * self.density

        self.id = self.canvas.create_oval(self.x - self.radius, self.y - self.radius,
                                          self.x + self.radius, self.y + self.radius,
                                          fill=self.color, outline='')

    def canvas_collision(self):
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
        self.canvas_collision()
        self.vy += scene.g * scene.update_time
        self.y += self.vy * scene.update_time
        self.x += self.vx * scene.update_time
        self.canvas.coords(self.id, self.x - self.radius, self.y - self.radius,
                           self.x + self.radius, self.y + self.radius)


class Scene:
    def __init__(self, objects=[]):
        self.height = 1024
        self.width = 1024
        self.fps_limit = 100
        self.tick_time = 100 / self.fps_limit
        self.update_time = 0.2
        self.bg_color = 'black'
        self.g = 0
        self.objects = objects
        self.G = 5

        self.window = Tk()
        self.window.title('Engine')
        self.window.resizable(False, False)

        self.canvas = Canvas(self.window, bg=self.bg_color, height=self.height, width=self.width)
        self.canvas.pack()

    def add_ball(self, event):
        colors = ["white",
                  "cyan",
                  "magenta",
                  "red",
                  "blue",
                  "gray",
                  'green',
                  'orange'
                   ]
        radius = randint(1, 1)
        x = event.x
        y = event.y
        vx = randint(0, 0)
        vy = randint(0, 0)
        color = colors[randint(0, len(colors)-1)]
        new_ball = Ball(scene.canvas, radius=radius, coordinates=(x, y), speed=(vx, vy), color=color)
        self.objects.append(new_ball)

    def g_force(self, x1, y1, x2, y2, m2):
        phi = atan2(y2-y1, x2-x1)
        r_2 = (x2-x1)**2+(y2-y1)**2

        a = (scene.G * m2) / r_2
        ax = a * cos(phi)
        ay = a * sin(phi)
        return ax, ay

    def all_g_force(self, object):
        x = object.x
        y = object.y
        sum_ax = 0
        sum_ay = 0
        for obj in scene.objects:
            if object == obj:
                sum_ax += 0
                sum_ay += 0
            else:
                ax, ay = self.g_force(x, y, obj.x, obj.y, obj.mass)
                sum_ax += ax
                sum_ay += ay
        return sum_ax, sum_ay

    def update_by_grav(self, object):
        ax, ay, = self.all_g_force(object)
        dvx = ax / self.update_time
        dvy = ay / self.update_time

        object.vx += dvx
        object.vy += dvy

        object.x += object.vx * self.update_time
        object.y += object.vy * self.update_time

    def is_collision(self, object_1, object_2):

        l_2 = (object_2.x - object_1.x) ** 2 + (object_2.y - object_1.y) ** 2

        if object_1 != object_2 and l_2 <= (object_2.radius + object_1.radius)**2:
            return True
        else:
            return False

    def collision_depth(self, object_1, object_2):
        l = sqrt((object_2.x-object_1.x)**2+(object_2.y-object_1.y)**2)

        if l < object_2.radius + object_1.radius:
            phi = atan2(object_2.y - object_1.y, object_2.x - object_1.x)
            depth = object_2.radius + object_1.radius - l

            depth_x = depth*cos(phi)
            depth_y = depth*sin(phi)

            move_1x = depth_x / 2
            move_1y = depth_y / 2
            move_2x = move_1x
            move_2y = move_1y
        else:
            move_1x, move_1y, move_2x, move_2y = 0, 0, 0, 0

        return -move_1x, -move_1y, move_2x, move_2y

    def move_by_collision(self, object1):
        for object2 in scene.objects:
            if object1 == object2:
                continue
            elif self.collision_depth(object1, object2):
                move_1x, move_1y, move_2x, move_2y = self.collision_depth(object1, object2)
                object1.x += move_1x
                object1.y += move_1y
                object2.x += move_2x
                object2.y += move_2y

    def collide(self, obj1, obj2):

        if self.is_collision(obj1, obj2):

            vx1 = obj1.vx
            vy1 = obj1.vy
            v1 = sqrt(vx1 ** 2 + vy1 ** 2)
            m1 = obj1.mass
            theta1 = atan2(vy1, vx1)

            vx2 = obj2.vx
            vy2 = obj2.vy
            v2 = sqrt(vx2 ** 2 + vy2 ** 2)
            m2 = obj2.mass
            theta2 = atan2(vy2, vx2)

            phi = atan2((obj2.y - obj1.y), (obj2.x - obj1.x))

            v1x_new = ((v1 * cos(theta1 - phi) * (m1 - m2) + 2 * m2 * v2 * cos(theta2 - phi)) / (m1 + m2)) * cos(
                phi) + v1 * sin(theta1 - phi) * cos(phi + pi / 2)
            v1y_new = ((v1 * cos(theta1 - phi) * (m1 - m2) + 2 * m2 * v2 * cos(theta2 - phi)) / (m1 + m2)) * sin(
                phi) + v1 * sin(theta1 - phi) * sin(phi + pi / 2)

            v2x_new = ((v2 * cos(theta2 - phi) * (m2 - m1) + 2 * m1 * v1 * cos(theta1 - phi)) / (m1 + m2)) * cos(
                phi) + v2 * sin(theta2 - phi) * cos(phi + pi / 2)
            v2y_new = ((v2 * cos(theta2 - phi) * (m2 - m1) + 2 * m1 * v1 * cos(theta1 - phi)) / (m1 + m2)) * sin(
                phi) + v2 * sin(theta2 - phi) * sin(phi + pi / 2)

            obj1.vx, obj1.vy = v1x_new, v1y_new
            obj2.vx, obj2.vy = v2x_new, v2y_new

            obj1.x += obj1.vx * scene.update_time
            obj1.y += obj1.vy * scene.update_time
            obj2.x += obj2.vx * scene.update_time
            obj2.y += obj2.vy * scene.update_time

    def pro_collide(self, obj1, obj2):
        if self.is_collision(obj1, obj2):

            k = 0.1

            vx1 = obj1.vx
            vy1 = obj1.vy
            v1 = sqrt(vx1 ** 2 + vy1 ** 2)
            m1 = obj1.mass
            theta1 = atan2(vy1, vx1)

            vx2 = obj2.vx
            vy2 = obj2.vy
            v2 = sqrt(vx2 ** 2 + vy2 ** 2)
            m2 = obj2.mass
            theta2 = atan2(vy2, vx2)

            phi = atan2((obj2.y - obj1.y), (obj2.x - obj1.x))

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

            obj1.vx, obj1.vy = v1x_new, v1y_new
            obj2.vx, obj2.vy = v2x_new, v2y_new

            obj1.x += obj1.vx * scene.update_time
            obj1.y += obj1.vy * scene.update_time
            obj2.x += obj2.vx * scene.update_time
            obj2.y += obj2.vy * scene.update_time

    def collisions_manager(self):
        collisions = []

        for obj1 in self.objects:
            for obj2 in self.objects:
                if obj1 != obj2:
                    collisions.append(self.is_collision(obj1, obj2))
                    self.pro_collide(obj1, obj2)

        if any(collisions):
            for obj1 in self.objects:
                self.move_by_collision(obj1)


    def gravity_manager(self):
        for obj in self.objects:
            obj.update_coordinates()
            self.update_by_grav(obj)

    def next_frame(self):

        self.collisions_manager()
        self.gravity_manager()
        self.window.bind('<Button-1>', self.add_ball)
        self.canvas.update_idletasks()
        self.window.after(int(self.tick_time), self.next_frame)


    def loop(self):
        self.next_frame()
        self.window.mainloop()


scene = Scene()




ball_1 = Ball(scene. canvas, radius=1, coordinates=(0, 0), speed=(0, 0), mass=1, color='blue')
ball_2 = Ball(scene. canvas, radius=1, coordinates=(1024, 0), speed=(0, 0), mass=1, color='pink')
ball_3 = Ball(scene. canvas, radius=1, coordinates=(1024, 1024), speed=(0, 0), mass=1, color='red')
ball_4 = Ball(scene. canvas, radius=1, coordinates=(0, 1024), speed=(0, 0), mass=1, color='cyan')

scene.objects = [ball_1, ball_2, ball_3, ball_4]

scene.loop()


