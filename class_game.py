# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 22:38:24 2017

@author: Paule
"""

import pygame
import matplotlib.path as mplPath
import numpy as np
import math
import sys

disp = (1200,800)

class Game(object):
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.disp = (self.screen_rect[2],self.screen_rect[3])
        self.clock = pygame.time.Clock()
        self.myfont = pygame.font.SysFont('Comic Sans MS', 30)

        
        
        
        
        
    def start(self):
        crashed = False
        while not crashed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    crashed = True
            self.screen.fill((255,255,255))
            a = ant(50,40,0)
            a.show()
            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()

class ant(Game):
    def __init__(self,x,y,deg):
        Game.__init__(self)
        self.size = 50
        self.rotate = deg
        self.x =  x
        self.y = y
        self.cx = self.x + self.size/2
        self.cy = self.y + self.size/2
        self.startpoint = pygame.math.Vector2(self.cx, self.cy)
        self.endpoint = pygame.math.Vector2(0, -self.disp[0])



            
    def show(self):
        antImg = pygame.image.load('ant.png')
        antImg = pygame.transform.scale(antImg,(self.size,self.size))
        ant1 = self.rot_center(antImg,self.rotate)
        self.screen.blit(ant1,(self.x,self.y))
        
    def rot_center(self,image, angle):
        """rotate an image while keeping its center and size"""
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

class food(Game):
    pass
        
        
def main():
    pygame.init()
    pygame.display.set_mode(disp)
    pygame.display.set_caption('AntLife')
    g = Game()
    g.start()
    pygame.quit()
    sys.exit()
    
main()

    
    