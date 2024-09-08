from tkinter import Tk, Canvas
from random import randint
from math import atan2, cos, sin

class Ball:
    def __init__(self, canvas, radius, coordinates, speed=(0, 0), color='white', mass=1e-8):
        self.canvas = canvas
        self.radius = radius
        self.color = color
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.vx = speed[0]
        self.vy = speed[1]
        self.elasticity = 0.5
        self.friction = 0.999
        self.mass = mass

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
        else:
            self.vy += scene.g * scene.update_time
            self.y += self.vy * scene.update_time

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
        else:
            self.x += self.vx * scene.update_time

    def update_coordinates(self):
        self.canvas_collision()
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
        self.G = 10

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
        radius = randint(5, 10)
        x = event.x
        y = event.y
        vx = randint(1, 1)
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


    def next_frame(self):

            for object in self.objects:
                object.update_coordinates()
                self.update_by_grav(object)

            self.window.bind('<Button-1>', self.add_ball)
            self.canvas.update_idletasks()
            self.window.after(int(self.tick_time), self.next_frame)


    def loop(self):
        self.next_frame()
        self.window.mainloop()


scene = Scene()



sun = Ball(scene. canvas, radius=20, coordinates=(1024/2, 1024/2), speed=(0, 0), mass=1, color='yellow')
ball_1 = Ball(scene. canvas, radius=5, coordinates=(1024/2+100, 1024/2), speed=(0, -1), mass=1e-9, color='blue')
ball_1s = Ball(scene. canvas, radius=1, coordinates=(1024/2-300, 1024/2+15), speed=(-0.01, +0.60), mass=1e-11, color='blue')
ball_2 = Ball(scene. canvas, radius=5, coordinates=(1024/2-100, 1024/2), speed=(0, +1), mass=1e-9, color='cyan')
ball_3 = Ball(scene. canvas, radius=5, coordinates=(1024/2-200, 1024/2), speed=(0, +0.75), mass=1e-9, color='orange')
ball_4 = Ball(scene. canvas, radius=8, coordinates=(1024/2-300, 1024/2), speed=(0, +0.6), mass=1e-5, color='brown')
ball_5 = Ball(scene. canvas, radius=3, coordinates=(1024/2-400, 1024/2), speed=(0, +0.55), mass=5e-10, color='grey')

scene.objects = [sun, ball_1, ball_1s, ball_2, ball_3, ball_4, ball_5]

scene.loop()


