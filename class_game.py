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
import random



disp = (1200,800)

class Game(object):
    

    
    def __init__(self):
        Game.screen = pygame.display.get_surface()
        Game.screen_rect = Game.screen.get_rect()
        Game.disp = (Game.screen_rect[2],Game.screen_rect[3])
        Game.myfont = pygame.font.SysFont('Comic Sans MS', 10)
        Game.food_data = []
        Game.food_amount = 0
        Game.food_dic = {}
        
        self.FPS = 60
        self.clock = pygame.time.Clock()
        self.prob = 1
        self.spawn_food
        self.food_target = 10


    def decision(self,probability):
        return random.random() < probability
    
    def get_key(self):
        low = 0
        keys = [int(i) for i in list(Game.food_dic.keys())]
        for i in range(self.food_target):
            if low in keys:
                low +=1
            else:
                return low

    def spawn_food(self):
        x_loc = random.randint(0,self.disp[0])
        y_loc = random.randint(0,self.disp[1])
        loc = [x_loc,y_loc]
        Game.food_data.append(loc)   
        key = self.get_key()
        Game.food_dic[str(key)]=food(*loc)
        Game.food_amount = len(Game.food_dic)
        print(food.num_food)
        print("spawned")
    
    def destroy_food(self, num=None):
        if num is not None:
            pass
        else:
            num = np.random.choice(list(Game.food_dic.keys()))
            del Game.food_dic[num]
            food.num_food -= 1
            Game.food_amount = len(Game.food_dic)
            print("destroyed")
        
        
    def monitor_food(self,num, dis_chance):
        if Game.food_amount > 1:
            if self.decision(dis_chance/self.FPS):
                self.destroy_food()
        if self.decision((1-self.prob)/self.FPS):
                self.spawn_food()
        self.prob = Game.food_amount/(num)
        for i in list(Game.food_dic.keys()):
            Game.food_dic[i].show()
        
        
    def start(self):
        
        self.a = ant(50,40,260)
        self.b = ant(300,200,180)
        self.c = ant(500,500,270)
        
        
        crashed = False
        while not crashed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    crashed = True
            self.screen.fill((255,255,255))


#            self.a.update(self.food_data)
#            self.b.update(self.food_data)
#            self.c.update(self.food_data)
            self.a.update()
            self.b.update()
            self.c.update()
            
            self.monitor_food(self.food_target,0.1)
            
            pygame.display.update()
            self.clock.tick(self.FPS)

        pygame.quit()

class ant(Game):
    num_ants = 0
    
    def __init__(self,x,y,deg):
        ant.num_ants += 1
#        Game.__init__(self)
        self.size = 30
        self.FoV_size = 50
        self.FoV_length = 800
        self.rotate = deg
        self.x =  x
        self.y = y
        self.cx = self.x + self.size/2
        self.cy = self.y + self.size/2
        self.startpoint = pygame.math.Vector2(self.cx, self.cy)
#        self.endpoint = pygame.math.Vector2(0, -self.disp[0])
        self.endpoint = pygame.math.Vector2(0, -self.FoV_length)
        self.health = 100
        
        antImg = pygame.image.load('ant.png')
        self.antImg = pygame.transform.scale(antImg,(self.size,self.size))

    
    def update(self):
        #life update
        self.check_FoV(draw=True)
        self.show()

    def health_update(self):
        pass
    
    
    def check_FoV(self,draw = False):
        right = 360+self.FoV_size/2-self.rotate
        left = 360-self.FoV_size/2-self.rotate
        current_endpoint1 = self.startpoint + self.endpoint.rotate(right)
        current_endpoint2 = self.startpoint + self.endpoint.rotate(left)
        if draw == True:
            pygame.draw.line(
            self.screen, (255,0,0), self.startpoint, current_endpoint1, 2)
            pygame.draw.line(
            self.screen, (255,0,0), self.startpoint, current_endpoint2, 2)

        d1 = [self.cx, self.cy]
        d2 = list(current_endpoint1)
        d3 = list(current_endpoint2)
        ar = np.array([d1,d2,d3])
        bbPath = mplPath.Path(ar)
        contained =  []
        found = False
        for i in self.food_data:
            if bbPath.contains_point(i) == True:
                found = True
                fx,fy = i
                dist = int(math.sqrt((fx-self.cx)**2 + (fy-self.cy)**2)-self.size/2)
                contained.append(dist)
        if found == True:
            label = self.myfont.render(str(contained), 1, (0,0,0))
            x_coords = label.get_rect().width / 2
            self.screen.blit(label, (self.cx-x_coords, self.cy-(self.size*0.8)))

            
    def show(self):
        ant1 = self.rot_center(self.antImg,self.rotate)
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
    num_food = 0
    
    def __init__(self,x,y):

        self.x = x
        self.y = y
        self.show()
        food.num_food += 1
        
    def show(self):
        pygame.draw.circle(self.screen,(0,0,255),(self.x,self.y),5)
        
        
        
        
def main():
    pygame.init()
    pygame.display.set_mode(disp)
    pygame.display.set_caption('AntLife')
    g = Game()
    g.start()
    pygame.quit()
    sys.exit()
    
main()

    
    