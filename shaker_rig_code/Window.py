#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 16:26:04 2022

@author: eli
"""
from Plot import Plot
import pygame
import pygame_gui

WIDTH, HEIGHT = 1000, 500

class Window:
    
    def __init__(self, shaker):
        self.window = pygame.display
        self.running = True
        self.shaker = shaker
        self.setup_ui()
        self.plot_area = (350,50,600,400)
        self.plot = Plot(self.screen, *self.plot_area )
        self.loop()

    
    def loop(self):    
        while self.running:
            # get user input
            time_delta = self.clock.tick(60)/1000.0
            
            for event in pygame.event.get():
                # close window if clicked (x)
                if event.type == pygame.QUIT:
                    self.running = False
                    self.shaker.end_game()
                            
                if (event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == '#frequency_input'):
                    self.shaker.set_tone_frequency(float(event.text))    
                if (event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == '#amplitude_input'):
                    self.shaker.set_tone_amplitude(float(event.text))
                
                if (event.type == pygame_gui.UI_BUTTON_PRESSED):
                    print('button pressed')
                    if (event.ui_element == self.button_play):
                        print('Play Pressed')
                        self.shaker.play_tone()
                
                    if (event.ui_element == self.button_pause):
                        print('Pause Pressed')
                        self.shaker.pause_tone()
                
                
                self.ui_manager.process_events(event)
                       
            self.ui_manager.update( time_delta )
            self.plot.update( time_delta )
            # Fill the background with white
            #self.screen.fill("white")
            self.ui_manager.draw_ui(self.screen)
            pygame.display.update()
        
        #Done! Time to quit.
        pygame.quit()
        

      

    
    def setup_ui(self):
        self.screen = self.window.set_mode([WIDTH, HEIGHT])
        self.screen.fill("white")
        self.window.set_caption('Harris Lab Shaker Control')
        self.clock = pygame.time.Clock()
        self.ui_manager = pygame_gui.UIManager((WIDTH,HEIGHT))
        self.freq_input_line = pygame_gui.elements.UITextEntryLine(relative_rect=((50,100),(250,40)), manager=self.ui_manager, object_id='#frequency_input' )
        self.amp_input_line = pygame_gui.elements.UITextEntryLine(relative_rect=((50,200),(250,40)), manager=self.ui_manager, object_id='#amplitude_input' )
        self.label_freq = pygame_gui.elements.UILabel(relative_rect=(pygame.Rect(50,50,200,40)), text='Input Frequency (Hz)', manager=self.ui_manager)
        self.label_amp = pygame_gui.elements.UILabel(relative_rect=(pygame.Rect(50,150,200,40)), text='Input Amplitude (0-1)',manager=self.ui_manager)
        
        self.button_play = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50,250),(100,40)), text="Play", manager=self.ui_manager)
        self.button_pause = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((200,250),(100,40)), text="Pause", manager=self.ui_manager)
        