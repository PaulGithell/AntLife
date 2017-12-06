# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 19:40:21 2017

@author: Paule
"""

import pygame
import matplotlib.path as mplPath
import numpy as np
import math


pygame.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)


display_width = 1200
display_height = 800
size_x = 50
size_y = 50
rotate = 0


gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('A bit Racey')

black = (0,0,0)
white = (255,255,255)

clock = pygame.time.Clock()
crashed = False
carImg = pygame.image.load('ant.png')
carImg = pygame.transform.scale(carImg,(size_x,size_y))

def cars(x,y,deg):
    a = pygame.transform.rotate(carImg,deg)
    gameDisplay.blit(a, (x,y))
    
    
x =  int(round(display_width * 0.5))
y = int(round(display_height * 0.5))
cx = x + size_x/2
cy = y + size_y/2

startpoint = pygame.math.Vector2(cx, cy)
endpoint = pygame.math.Vector2(0, -1200)

def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

def check_FoV(car,end1,end2,fx,fy,x,y):
    cx = car.get_rect().center[0]+x
    cy = car.get_rect().center[1]+y
    d1 = [cx, cy]
    d2 = list(end1)
    d3 = list(end2)
    ar = np.array([d1,d2,d3])
    bbPath = mplPath.Path(ar)
    if bbPath.contains_point((fx,fy)) == True:
        dist = int(math.sqrt((fx-cx)**2 + (fy-cy)**2)-size_x/2)
        label = myfont.render(str(dist), 1, (0,0,0))
        gameDisplay.blit(label, (cx, cy-70))
        
fx = int(display_width * 0.4)
fy = int(display_width * 0.4)

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            rotate += 5


                        if event.key == pygame.K_RIGHT:
                            rotate -= 5

         
#                    if event.type == pygame.KEYUP:
#                        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
#                            x_change = 0

    gameDisplay.fill(white)
    pygame.draw.circle(gameDisplay,(0,0,255),(fx,fy),5)


    current_endpoint1 = startpoint + endpoint.rotate(380-rotate)
    current_endpoint2 = startpoint + endpoint.rotate(340-rotate)
    pygame.draw.line(
        gameDisplay, (255,0,0), startpoint, current_endpoint1, 2)
    pygame.draw.line(
        gameDisplay, (255,0,0), startpoint, current_endpoint2, 2)
    #car(x,y,rotate)
    car = rot_center(carImg,rotate)
    gameDisplay.blit(car,(x,y))
    check_FoV(car,current_endpoint1,current_endpoint2,fx,fy,x,y)
#    


        
    pygame.display.update()
    clock.tick(60)

pygame.quit()

