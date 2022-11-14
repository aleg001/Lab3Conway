"""
OpenGL en pygame
Author: Alecraft Gomez
Fecha: 25/10/2022
"""

"""
Simplificación del mundo en el que vivimos.
Un mundo dentro de un mundo.

Cada impacto que producimos de forma individual
puede desencadenar cambios sin predecir

El juego de la vida tiene un comienzo y un fin.

¡¡RIP CONWAY!!

"""

"""
Referencias:
https://www.youtube.com/watch?v=omMcrvVGTMs&ab_channel=DotCSV
https://beltoforion.de/en/recreational_mathematics/game_of_life.php 
https://www.pygame.org/docs/ref/surface.html#pygame.Surface.set_at
https://www.pygame.org/docs/ref/surface.html#pygame.Surface.get_at
https://www.youtube.com/watch?v=NDXyRhTYidQ&ab_channel=GetIntoGameDev
https://www.youtube.com/watch?v=2iyx8_elcYg&ab_channel=CodingWithRuss
https://www.youtube.com/watch?v=0XI6s-TGzSs&ab_channel=GarrettKoller
https://www.youtube.com/watch?v=FWSR_7kZuYg&ab_channel=TheCodingTrain
https://www.youtube.com/watch?v=lk1_h2_GLv8&ab_channel=CoderSpace
https://www.youtube.com/watch?v=d73z8U0iUYE&ab_channel=Auctux
"""


# Referencia de musica
# https://www.askpython.com/python-modules/pygame-adding-background-music

# Imports
import math
import sys
import time
import pygame as glfw
from OpenGL.GL import *
from numpy import *
import random
from pygame import mixer

# Constantes de tamaño de pantalla

w = 600
h = 600

# Colores parecidos a los propuestos en canvas
purple = (0.2, 0, 0.2)
yellow = (1, 1, 0.5)


# Configuracion inicial
glfw.init()
window = glfw.display.set_mode((w, h), glfw.OPENGL | glfw.DOUBLEBUF)
glfw.mouse.set_pos(w / 2, h / 2)
glfw.display.set_caption("Lab 3 - El Juego del Conway")

# Musica
mixer.init()
mixer.music.load("Conway.mp3")
mixer.music.play(loops=1000)

"""
Se define una función para escribir la lista de coordenadas
en un archivo de texto
"""


def EscribirPuntosTexto(lista):
    with open("Conway.txt", "w") as filehandle:
        for listitem in lista:
            filehandle.write("%s\n" % listitem)


# Se definen los puntos iniciales
Coordenadas = [
    [80, 50],
    [90, 50],
    [100, 50],
    [100, 60],
    [90, 70],
    [130, 100],
    [500, 100],
    [150, 100],
    [150, 110],
    [140, 120],
    [50, 100],
    [60, 100],
    [70, 100],
    [180, 150],
    [190, 150],
    [200, 150],
    [200, 160],
    [190, 170],
]


randomNumber = random.randint(1, 5)

# Generacion de figuras "aleatorias" siguiendo algunos patrones comunes de Conway
for i in range(0, randomNumber):
    # Generacion de varios numberos random para la posicion de los puntos
    randomNumber2 = random.randint(100, 200)
    Coordenadas.append([180 + randomNumber2, 150 + randomNumber2])
    Coordenadas.append([190 + randomNumber2, 150 + randomNumber2]),
    Coordenadas.append([200 + randomNumber2, 150 + randomNumber2]),
    Coordenadas.append([200 + randomNumber2, 160 + randomNumber2]),
    Coordenadas.append([190 + randomNumber2, 170 + randomNumber2]),

    Coordenadas.append([90 + randomNumber2, 75 + randomNumber2])
    Coordenadas.append([95 + randomNumber2, 75 + randomNumber2]),
    Coordenadas.append([100 + randomNumber2, 76 + randomNumber2]),
    Coordenadas.append([100 + randomNumber2, 80 + randomNumber2]),
    Coordenadas.append([95 + randomNumber2, 85 + randomNumber2]),


# Defincion de array vacio
limitesPantalla = []
# Constantes
x = 0

funcionar = True
inicial = 0

inicialB = 24
inicialC = 74


# Agregar otra figura random
figuraRandom = random.choice([inicialB, inicialC])


for i in range(0, 5):
    Coordenadas.append([inicial + i, figuraRandom])


def ClearWait():
    FlipScreen()
    time.sleep(1.5)


# Draw a pixel
def pixel(x, y, color):
    glEnable(GL_SCISSOR_TEST)
    glScissor(x, y, 9, 9)
    glClearColor(color[0], color[1], color[2], 1)
    glClear(GL_COLOR_BUFFER_BIT)
    glDisable(GL_SCISSOR_TEST)


# Draw a bar
def pixelBar(x, y, color):
    glEnable(GL_SCISSOR_TEST)
    glScissor(x, y, 10, 100)
    glClearColor(color[0], color[1], color[2], 1)
    glClear(GL_COLOR_BUFFER_BIT)
    glDisable(GL_SCISSOR_TEST)


# Clean screen
def CleanScreen():
    glClearColor(0.0, 0, 0.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT)


# Flip framebuffer
def FlipScreen():
    glfw.display.flip()


# Algoritmo principal
def conwayGameOfLife(celdas, tamano, actualizarse):

    shapeTuple = (celdas.shape[0], celdas.shape[1])
    celulasVacias = zeros(shapeTuple)
    """
    An N-dimensional iterator object to index arrays.
    Given the shape of an array, an ndindex instance iterates over the N-dimensional index of the array. 
    At each iteration a tuple of indices is returned, the last dimension is iterated over first.
    """

    """
    The shape attribute for numpy arrays returns the dimensions of the array.
    If Y has n rows and m columns, then Y.shape is (n,m). So Y.shape[0] is n.
    """

    for i, j in ndindex(celdas.shape[0], celdas.shape[1]):
        tempValue1 = i - 1
        tempValue2 = j - 1
        tempValue3 = i + 2
        tempValue4 = j + 2

        # Referencia de slices en python:
        # https://stackoverflow.com/questions/44633798/what-is-the-meaning-of-list-in-this-code
        celdasVivas = sum(celdas[tempValue1:tempValue3, tempValue2:tempValue4])
        celdasVivas = celdasVivas - celdas[i, j]

        if celdas[i, j] == 0:
            color = purple
        else:
            color = yellow

        if celdas[i, j] == 1:
            if celdasVivas < 2:
                if actualizarse == True:
                    color = purple
            if celdasVivas > 3:
                if actualizarse == True:
                    color = purple

            if celdasVivas <= 3:
                celulasVacias[i, j] = 1
                if actualizarse == True:
                    color = yellow
            if celdasVivas >= 2:
                celulasVacias[i, j] = 1
                if actualizarse == True:
                    color = yellow
        else:
            if celdasVivas == 3:
                celulasVacias[i, j] = 1
                if actualizarse == True:
                    color = yellow

        var1 = i * tamano
        var2 = j * tamano
        pixel((var2), (var1), (color))

    return celulasVacias


w1 = glfw.display.get_window_size()[0]
h1 = glfw.display.get_window_size()[1]
numberOfZerosW = round(w1 / 10)
numberOfZerosH = round(h1 / 10)
numberOfZeros = (numberOfZerosW, numberOfZerosH)
CELDAS = zeros(numberOfZeros)
conwayGameOfLife(CELDAS, 10, False)
FlipScreen()
for i in Coordenadas:
    firstDivision = i[0] / 10
    secondDivision = i[1] / 10
    # Referencia para aproximar al siguiente entero:
    # https://www.freecodecamp.org/news/how-to-round-numbers-up-or-down-in-python/#:~:text=ceil()%20method%20rounds%20a,accessible%20through%20the%20math%20module.
    firstDivision = math.ceil(firstDivision)
    secondDivision = math.ceil(secondDivision)
    CELDAS[secondDivision, firstDivision] = 1
    conwayGameOfLife(CELDAS, 10, False)
    FlipScreen()

celdasFuncionando = False

# Until window is closed
# Referencia para el cierre de la ventana
# https://stackoverflow.com/questions/19882415/closing-pygame-window
try:
    while funcionar:
        for e in glfw.event.get():
            if e.type == glfw.QUIT:
                funcionar = False
                glfw.quit()
                sys.exit()
            else:
                celdasFuncionando = True
                conwayGameOfLife(CELDAS, 10, False)

            glClear(GL_COLOR_BUFFER_BIT)
            if celdasFuncionando == True:
                CELDAS = conwayGameOfLife(CELDAS, 10, True)
                ClearWait()

except SystemExit:
    glfw.quit()

EscribirPuntosTexto(Coordenadas)
