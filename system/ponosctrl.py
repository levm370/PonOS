from system.ponosgraphics import *
import math
def ponos(obj):
    objects = obj
    renderer = Renderer(objects)
    updater = Updater(objects)
    return renderer, updater
def square(x, y, w, h):
    return GameObject(x, y, w, h)
def startall(r, u):
    ml = MainLoop(r, u)
    ml.start()

center_x, center_y = 200, 200  # центр круга
radius = 100  # радиус круга
num_squares = 10  # количество квадратов (чем больше, тем более гладкий круг)

objects = []
def circle():
    global objects
    for i in range(num_squares):
        # Вычисляем координаты точки на окружности
        angle = 2 * math.pi * i / num_squares
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
    
        # Добавляем квадрат в список объектов
        objects.append(square(x, y, 10, 10))

        rnd, upd = ponos(objects)
        startall(rnd, upd)
