from tkinter import *
from random import randint

class Ball:
    def __init__(self, canvas, radius, coordinates, speed=(0, 0), color='white', mass=1):
        self.canvas = canvas
        self.radius = radius
        self.color = color
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.vx = speed[0]
        self.vy = speed[1]
        self.elasticity = 1
        self.friction = 1
        self.mass=1

        self.id = self.canvas.create_oval(self.x - self.radius, self.y - self.radius,
                                          self.x + self.radius, self.y + self.radius,
                                          fill=self.color)

    def update_coordinates(self):

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


        self.canvas.coords(self.id, self.x - self.radius, self.y - self.radius,
                           self.x + self.radius, self.y + self.radius)


class Scene:
    def __init__(self, objects=[]):
        self.height = 640
        self.width = 1024
        self.fps_limit = 1000
        self.tick_time = 1000 / self.fps_limit
        self.update_time = self.tick_time/60
        self.bg_color = 'black'
        self.g = 9.8
        self.objects = objects

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
        radius = randint(5, 50)
        x = event.x
        y = event.y
        vx = randint(-100, 100)
        vy = randint(-100, 100)
        color = colors[randint(0, len(colors)-1)]
        new_ball = Ball(scene.canvas, radius=radius, coordinates=(x, y), speed=(vx, vy), color=color)
        self.objects.append(new_ball)

    def next_frame(self):
        #self.canvas.delete('all')
        for object in self.objects:
            object.update_coordinates()
        self.window.bind('<Button-1>', self.add_ball)
        self.window.after(int(self.tick_time), self.next_frame)

    def loop(self):

        self.next_frame()
        self.window.mainloop()

scene = Scene()

scene.loop()


