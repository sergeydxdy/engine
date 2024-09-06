from tkinter import *


height = 640
width = 1024
fps_limit = 120
tick_time = int(1000 / fps_limit)
bg_color = 'black'
g = 9.8

window = Tk()
window.title('Engine')
window.resizable(False, False)

canvas = Canvas(window, bg=bg_color, height=height, width=width)
canvas.pack()

window.update()


class Ball():
    def __init__(self, radius, coordinates, speed=(0, 0)):
        self.radius = radius
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.vx = speed[0]
        self.vy = speed[1]

        canvas.create_oval(self.x-self.radius, self.y-self.radius, self.x + self.radius, self.y + self.radius, fill='white')


    def update_coordinates(self):
        vx = self.vx
        vy = self.vy + g * tick_time
        x = self.x + (tick_time * self.vx)*0.001
        y = self.y + (tick_time * self.vy)*0.001
        return vx, vy, x, y

def next_frame(objects):
    updated_objects = []
    canvas.delete('all')
    for object in objects:
        vx, vy, x, y = object.update_coordinates()
        object = Ball(object.radius, (x, y), speed=(vx, vy))
        updated_objects.append(object)
    window.after(tick_time, next_frame, updated_objects)


ball = Ball(10, (100, 300), speed=(1, 0))
ball1 = Ball(10, (500, 300), speed=(1, 0))
objects = [ball, ball1]
next_frame(objects)
window.mainloop()