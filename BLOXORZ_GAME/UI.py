import pygame as pg
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
import cv2
import numpy as np


class draw:
    def __init__(self, map, location, isSplit):
        self.cubeVertices = ((1,1,1),(1,1,0),(1,0,0),(1,0,1),(0,1,1),(0,0,0),(0,0,1),(0,1,0))
        self.cubeEdges = ((0,1),(0,3),(0,4),(1,2),(1,7),(2,5),(2,3),(3,6),(4,6),(4,7),(5,6),(5,7))
        self.cubeQuads = ((0,3,6,4),(2,5,6,3),(1,2,5,7),(1,0,4,7),(7,4,6,5),(2,3,0,1))
        self.texture = None
        self.map = map
        self.location = location
        self.isSplit = isSplit
        self.imgs = ['Plaster-Wall-Base', 'O', 'X', 'T']
        self.loadimgae()

    def update(self, map, location, isSplit):
        self.map = map
        self.location = location
        self.isSplit = isSplit

    def loadimgae(self):       
        self.texture = glGenTextures(4)
        for i in range(4):
            im = cv2.imread('images/' + self.imgs[i] + '.jpg')
            im=cv2.flip(im,0)
            im=cv2.cvtColor(im,cv2.COLOR_BGR2RGB)
            im=im.astype(np.float32)
            glBindTexture(GL_TEXTURE_2D, self.texture[i])
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, im.shape[0], im.shape[1], 0, GL_RGB, GL_UNSIGNED_BYTE, im)
        
    def texture_img(self, x, y, i):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture[i])
        glBegin(GL_QUADS)
        glTexCoord2f(0.0,0.0); glVertex3fv((x, y, 0.2))
        glTexCoord2f(1.0,0.0); glVertex3fv((1 + x, y, 0.2))
        glTexCoord2f(1.0,1.0); glVertex3fv((1 + x, 1 + y, 0.2))
        glTexCoord2f(0.0,1.0); glVertex3fv(( x, 1 + y, 0.2))
        glEnd()  
        glDisable(GL_TEXTURE_2D) 


    def drawText(self, x, y, text):      
        font = pg.font.SysFont('arial', 35)                                          
        textSurface = font.render("Press space to start!   " + "Step: " + str(text), True, (0, 0, 0, 0), ( 0, 255, 255, 0))
        textData = pg.image.tostring(textSurface, "RGBA", True)
        glWindowPos2d(x, y)
        glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

    def draw_map(self):
        y = len(self.map) // 2 + 3
        x = len(self.map[0]) // 2

        clone_y = y
        for i in range(len(self.map)):
            clone_x = x
            for j in range(len(self.map[0])):
                if self.map[i][j].type == '1':
                    self.box(j - clone_x, clone_y, (0.8, 0.8, 0.8), True)
                    self.texture_img(j - clone_x, clone_y, 0)
                if self.map[i][j].type == 'C':
                    self.box(j - clone_x, clone_y, (1, 0.5, 0.0), False)
                if self.map[i][j].type == 'O':
                    self.box(j - clone_x, clone_y, (0.8, 0.8, 0.8), True)
                    self.texture_img(j - clone_x, clone_y, 1)
                if self.map[i][j].type == 'X':
                    self.box(j - clone_x, clone_y, (0.8, 0.8, 0.8), True)
                    self.texture_img(j - clone_x, clone_y, 2)
                if self.map[i][j].type == 'T':
                    self.box(j - clone_x, clone_y, (0.8, 0.8, 0.8), True)
                    self.texture_img(j - clone_x, clone_y, 3)
            clone_y -= 1
        self.block(x, y)
        glFlush()


    def box(self, x, y, color, texture):
        glBegin(GL_QUADS)
        glColor(color)
        for cubeQuad in self.cubeQuads:
            for cubeVertex in cubeQuad:
                if cubeVertex == 0:
                    if texture == True:
                        continue
                glVertex3fv((self.cubeVertices[cubeVertex][0] + x, self.cubeVertices[cubeVertex][1] + y, self.cubeVertices[cubeVertex][2] * 0.2))
        glEnd()

        glBegin(GL_LINES)
        glColor(1, 1, 1)
        for cubeEdge in self.cubeEdges:
            for cubeVertex in cubeEdge:
                glVertex3fv((self.cubeVertices[cubeVertex][0] + x, self.cubeVertices[cubeVertex][1] + y, self.cubeVertices[cubeVertex][2] * 0.2))        
        glEnd()
        glLineWidth(1)

    def draw_block(self, x, y, location, size_x, size_y, height):
        i, j = location
        glBegin(GL_QUADS)
        glColor3f(1,0,0)
        for cubeQuad in self.cubeQuads:
            for cubeVertex in cubeQuad:
                if self.cubeVertices[cubeVertex][2] == 0:
                    glVertex3fv((self.cubeVertices[cubeVertex][0] * size_x + j - x, self.cubeVertices[cubeVertex][1] * size_y  + y - i, self.cubeVertices[cubeVertex][2] + 0.2))
                else:
                    glVertex3fv((self.cubeVertices[cubeVertex][0] * size_x + j - x, self.cubeVertices[cubeVertex][1] * size_y + y - i, self.cubeVertices[cubeVertex][2] + height))
        glEnd()

        glBegin(GL_LINES)
        glColor(1, 1, 1)
        for cubeEdge in self.cubeEdges:
            for cubeVertex in cubeEdge:
                if self.cubeVertices[cubeVertex][2] == 0:
                    glVertex3fv((self.cubeVertices[cubeVertex][0] * size_x + j - x, self.cubeVertices[cubeVertex][1] * size_y  + y - i, self.cubeVertices[cubeVertex][2] + 0.2))
                else:
                    glVertex3fv((self.cubeVertices[cubeVertex][0] * size_x + j - x, self.cubeVertices[cubeVertex][1] * size_y + y - i, self.cubeVertices[cubeVertex][2] + height))       
        glEnd()
        glLineWidth(2)

    def block(self, x, y):
        if len(self.location) == 1:
            self.draw_block(x, y, self.location[0], 1, 1, 1.2)
        else:
            if not self.isSplit:
                if self.location[0][0] == self.location[1][0]:
                    if self.location[0][1] < self.location[1][1]:
                        self.draw_block(x, y, self.location[0], 2, 1, 0.2)
                    else:
                        self.draw_block(x, y, self.location[1], 2, 1, 0.2)
                else:
                    if self.location[0][0] > self.location[1][0]:
                        self.draw_block(x, y, self.location[0], 1, 2, 0.2)
                    else:
                        self.draw_block(x, y, self.location[1], 1, 2, 0.2)
            else:
                for i in range(2):
                    self.draw_block(x, y, self.location[i], 1, 1, 0.2)

class UI:
    def __init__(self, map, listState = None):
        self.map = map
        self.listState = listState
        self.count = 0
        pg.init()
        display = (1000, 600)
        pg.display.set_caption('BLOXORZ')
        pg.display.set_mode(display, DOUBLEBUF|OPENGL)
        gluPerspective(50, (display[0]/display[1]), 0.1, 80.0)
        gluLookAt(-3, -7, 6, -1, -1, 0, 0, 0, 1)
        
        glEnable(GL_LINE_SMOOTH)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glTranslatef(0.0, 0.0, -5)
    
    def surface(self, object):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        object.drawText(10,550, self.count)
        object.draw_map()
    
    def run(self):
        m = draw(self.map, self.listState[0].location, False)
        self.listState = self.listState[1:]
        glClearColor(0, 1, 1, 0)
        self.surface(m)
        pg.display.flip()
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        pg.time.delay(50)
                        while len(self.listState) != 0:

                            m.update(self.listState[0].map, self.listState[0].location, self.listState[0].isSplit)
                            self.count += 1
                            self.listState = self.listState[1:]
                            self.surface(m)
                            pg.display.flip()
                            pg.time.delay(100)
                            if len(self.listState) == 1:
                                print("Solution is found!")

