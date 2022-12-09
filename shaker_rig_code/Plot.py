#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 16:34:51 2022

@author: eli
"""
import pygame
import random
import math

class Plot:
    
    def __init__(self, screen, x, y, width, height):
        # x bounds are between 0 and width
        # y bounds are between -height/2 and height/2
        self.plot_area = (x,y,width,height)
        self.screen = screen
        self.plt_width = width
        self.plt_height = height
        self.plt_offset = [x,y+height//2]
        
        self.x_scale = 1
        self.y_scale = 1
        self.total_time = 0
        self.x_pix_per_sec = 30
        
        self.x_max_points = 50 #self.plt_width // (self.x_scale * self.x_pix_per_sec) - 1
        

        
        self.ax_queue = []
        self.ay_queue = []
        self.az_queue = []
        
        self.draw_trace(self.ax_queue,'red')
        
    def update(self, time_delta):
        self.total_time += time_delta
        self.draw_background()
        
        #self.add_point('ax',self.total_time, random.randint(5, self.plt_height-5)-self.plt_height//2)
        #self.add_point('ay', self.total_time, random.randint(5, self.plt_height-5)-self.plt_height//2)        
        #self.add_point('az', self.total_time, random.randint(5, self.plt_height-5)-self.plt_height//2)
        self.add_point('ax',self.total_time, math.sin(self.total_time * 2 * math.pi / 3)* 100)
        self.add_point('ay',self.total_time, math.sin(self.total_time * 2 * math.pi / .5)* 100)
        self.add_point('az',self.total_time, math.sin(self.total_time * 2 * math.pi / 1)* 100)
        
        self.update_trace('ax')
        self.update_trace('ay')
        self.update_trace('az')
        
        

    def draw_background(self):
         pygame.draw.rect(self.screen,'grey',self.plot_area)
         num_vert_lines =  5
         vert_lines=[]
         for i in range(num_vert_lines):
             y_val = i * self.plt_height/num_vert_lines
             self.draw_line('black',0,y_val,self.plt_width,y_val )
             
             
    def add_point(self, trace, x, y):
        if trace == 'ax':
            queue = self.ax_queue
        if trace == 'ay':
            queue = self.ay_queue
        if trace == 'az':
            queue = self.az_queue
        queue.append((x,y))
        
        

    def draw_trace(self, queue, color):
        pix_queue = self.coords_to_pixels(queue)
        for point in pix_queue:
            pygame.draw.circle(self.screen, color, point, 3)
        if len(pix_queue)>=2:
            pygame.draw.aalines(self.screen, color, False ,pix_queue)

        
    def update_trace(self,trace):
        if trace == 'ax':
            self.draw_trace(self.ax_queue,'red')
            return self.ax_queue
        if trace == 'ay':
            self.draw_trace(self.ay_queue, 'green')
            return self.ay_queue
        if trace == 'az':
            self.draw_trace(self.az_queue, 'blue')
            return self.az_queue

  
    def coords_to_pixels(self, coord_queue):
        pix_queue = []
        x_pix_offset = self.total_time * self.x_pix_per_sec
        pop_list=[]
        for i in range(len(coord_queue)):
            point = coord_queue[i]
            pix_x = self.plt_width + self.plt_offset[0] + (point[0] * self.x_pix_per_sec) - x_pix_offset - 5
            pix_y = self.plt_offset[1] - point[1]
            if pix_x > self.plt_offset[0] + 5:
                pix_queue.append([pix_x, pix_y])
            else:
                pop_list.append(coord_queue[i])
        for point in pop_list:    
            coord_queue.remove(point)
        return pix_queue

    def draw_line(self, color, x1,y1,x2,y2):
        pygame.draw.aaline(self.screen, color, (self.plt_offset[0]+ x1,self.plt_offset[1]+self.plt_height-y1),(self.plt_offset[0]+ x2,self.plt_offset[1]+self.plt_height-y2))