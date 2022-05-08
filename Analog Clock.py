import math
import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from datetime import *
from time import *

#################################
######## Constants ##############
#################################

xcenter = 0  # centre of circle
ycenter = 0
radius = .99  # radius of circle
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
FONT_DOWNSCALE = 0.0007


##########################################################################################


#################################
######## Initilization ##########
#################################

def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glPointSize(4.0)
    glMatrixMode(GL_PROJECTION)
    glOrtho(1, -1, 1, -1, 1, -1)
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW)


##########################################################################################

#################################
######## Circle #################
#################################

def draw_circle(xcenter, ycenter, radius, resolution=0.01, points=0, size=2, st_theta=0, end_theta=360):
    if points == 0:
        glLineWidth(size)
        glColor3f(0.0, 0.0, 0.0)
        glBegin(GL_LINE_STRIP)
    else:
        glPointSize(size)
        glColor3f(0.0, 0.0, 1.0)
        glBegin(GL_POINTS)
    for theta in np.arange(st_theta, end_theta, resolution):
        x = radius * math.cos(theta * math.pi / 180) + xcenter
        y = radius * math.sin(theta * math.pi / 180) + ycenter
        glVertex2d(x, y)
    glEnd()


##########################################################################################

###########################################################
######## fuction to draw lines of minutes #################
###########################################################

def draw_minutes():
    glLineWidth(3)
    glColor3f(0.0, 0.0, 1.0)
    for theta in np.arange(0, 360, 6):
        glBegin(GL_LINE_STRIP)
        x = 0.93 * math.cos(theta * math.pi / 180) + xcenter
        y = 0.93 * math.sin(theta * math.pi / 180) + ycenter
        glVertex2d(x, y)
        a = 0.89 * math.cos(theta * math.pi / 180) + xcenter
        b = 0.89 * math.sin(theta * math.pi / 180) + ycenter
        glVertex2d(a, b)
        glEnd()


##########################################################################################

##########################################################################
######## fuction to remove lines of minutes from numbers #################
##########################################################################

def remove_Lines():
    glColor3f(1, 1, 1)
    glBegin(GL_LINES)
    for theta in np.arange(0, 360, 30):
        x = 0.93 * math.cos(theta * math.pi / 180) + xcenter
        y = 0.93 * math.sin(theta * math.pi / 180) + ycenter
        a = 0.89 * math.cos(theta * math.pi / 180) + xcenter
        b = 0.89 * math.sin(theta * math.pi / 180) + ycenter
        glVertex2d(x, y)
        glVertex2d(a, b)
    glEnd()


##########################################################################################

########################################
######## Drawing Texts #################
########################################

def draw_text(string, x, y):
    glLineWidth(2)
    glColor(0, 0, 0)
    glPushMatrix()
    glTranslate(x, y, 0)
    glScale(FONT_DOWNSCALE, FONT_DOWNSCALE, 1)
    string = string.encode()  # conversion from Unicode string to byte string
    for c in string:
        glutStrokeCharacter(GLUT_STROKE_ROMAN, c)
    glPopMatrix()


##########################################################################################

##########################################
######## Drawing Numbers #################
##########################################

def draw_clock_numbers():
    num = 3
    glPushMatrix()
    for ang in range(0, 360, 30):
        x = 0.93 * math.cos(ang * math.pi / 180) - 0.02
        y = 0.93 * math.sin(ang * math.pi / 180) - 0.02
        if num == 12 or num == 11:
            y -= 0.01
            x -= 0.01
        draw_text(f"{num}", x, y)
        num -= 1
        if num <= 0:
            num += 12
    glPopMatrix()


##########################################################################################

#####################################
######## Clock hands animation ######
#####################################

def draw_hand(width, length, r, g, b):
    glLineWidth(width)
    glBegin(GL_LINE_STRIP)
    glColor3f(0.4, 0, 0.7)
    glVertex2d(0, 0)
    glColor3f(r, g, b)
    glVertex2d(0, length)
    glEnd()


def clock():
    # Getting Time from sys

    time = str(datetime.now().time()).split(':')
    sec = float(time[2])
    min = int(time[1]) + sec / 60
    hr = int(time[0]) + min / 60
    secondsHandRotation = sec * -6
    minutesHandRotation = min * -6
    if hr > 12:
        hr -= 12
    hoursHandRotation = hr * -30

    # Seconds Hand:

    glPushMatrix()
    glRotate(secondsHandRotation, 0, 0, 1)
    draw_hand(2, 0.93, 0, 1, 0)
    glPopMatrix()

    # Minutes Hand:

    glPushMatrix()
    glRotate(minutesHandRotation, 0, 0, 1)
    draw_hand(2, 0.83, 1, 0.8, 0.2)
    glPopMatrix()

    # Hours Hand:

    glPushMatrix()
    glRotate(hoursHandRotation, 0, 0, 1)
    draw_hand(5, 0.65, 0.8, 0.4, 1)
    glPopMatrix()

    # Center the text of hour markers

    currentT = datetime.now()
    h = currentT.hour
    if h > 12:
        h -= 12
        draw_text("PM", 0.27, -0.5)
    else:
        draw_text("AM", 0.27, -0.5)
    draw_text(str(h), -0.28, -0.5)
    draw_text(":", -0.15, -0.5)
    draw_text(str(currentT.minute), -0.09, -0.5)
    draw_text(":", 0.04, -0.5)
    draw_text(str(currentT.second), 0.12, -0.5)


##########################################################################################


def Display():
    glClearColor(1, 1, 1, 1)
    glClear(GL_COLOR_BUFFER_BIT)
    glEnable(GL_LINE_SMOOTH)
    glEnable(GL_BLEND)
    glEnable(GL_POLYGON_SMOOTH)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glLoadIdentity()
    draw_circle(xcenter, ycenter, radius)
    draw_minutes()
    remove_Lines()
    draw_circle(xcenter, ycenter, radius=0.93, resolution=1, points=1)
    draw_clock_numbers()
    clock()
    glutSwapBuffers()


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(50, 50)
    glutCreateWindow(b"Wall Clock")
    glutIdleFunc(Display)
    glutDisplayFunc(Display)
    init()
    glutMainLoop()


if __name__ == "__main__":
    main()