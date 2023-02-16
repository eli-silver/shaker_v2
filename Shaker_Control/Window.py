#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 16:26:04 2022

@author: eli
"""
import pygame
import pygame_gui

WIDTH, HEIGHT = 1000, 500


class Window:
    
    def __init__(self, display):
        self.display = display #pygame.display
        self.setup_ui()
        self.plot_area = (350,50,600,400)
    
    def get_plot_area(self):
        return self.plot_area
    
    def get_screen(self):
        return self.screen

    def get_ui_manager(self):
        return self.ui_manager
    
    def get_display(self):
        return self.display

    def setup_ui(self):
        self.screen = self.display.set_mode([WIDTH, HEIGHT])
        self.screen.fill("white")
        self.display.set_caption('Harris Lab Shaker Control')
        self.ui_manager = pygame_gui.UIManager((WIDTH,HEIGHT))
       
        self.freq_input_line = pygame_gui.elements.UITextEntryLine(relative_rect=((50,100),(250,40)), manager=self.ui_manager, object_id='#frequency_input' )
        self.vol_input_line = pygame_gui.elements.UITextEntryLine(relative_rect=((50,200),(250,40)), manager=self.ui_manager, object_id='#volume_input' )
        self.seq_path_input_line = pygame_gui.elements.UITextEntryLine(relative_rect=((50,350),(250,40)), manager=self.ui_manager, object_id='#seq_path_input')

        self.label_freq = pygame_gui.elements.UILabel(relative_rect=(pygame.Rect(50,50,200,40)), text='Input Frequency (Hz)', manager=self.ui_manager)
        self.label_vol = pygame_gui.elements.UILabel(relative_rect=(pygame.Rect(50,150,200,40)), text='Input Volume (0-100)',manager=self.ui_manager)
        self.label_seq_path = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(50,300,200,40), text='Tone Sequence File Path', manager=self.ui_manager)    
            
        self.button_play = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50,250),(100,40)), text="Play", manager=self.ui_manager)
        self.button_pause = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((200,250),(100,40)), text="Pause", manager=self.ui_manager)
        self.button_play_seq = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50,400),(250,40)), text='Start Sequence', manager=self.ui_manager)