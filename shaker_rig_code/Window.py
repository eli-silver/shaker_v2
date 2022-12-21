#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 16:26:04 2022

@author: eli
"""
from Plot import Plot
from Serial_Monitor import Serial_Monitor
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
        self.path = ''
        self.total_time = 0

        self.get_serial_input = False
        if self.get_serial_input:
            self.serial_monitor = Serial_Monitor(num_data_bytes = 2, num_traces=4)
            self.serial_monitor.serial_input_background_init()
        self.loop()

    
    def loop(self):    
        while self.running:
            # get user input
            time_delta = self.clock.tick(120)/1000.0
            
            for event in pygame.event.get():
                # close window if clicked (x)
                if event.type == pygame.QUIT:
                    self.running = False
                    if self.get_serial_input:
                        self.serial_monitor.close()
                    self.shaker.end_game()
                            
                if (event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == '#frequency_input'):
                    self.shaker.set_tone_frequency(float(event.text))    
                if (event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == '#volume_input'):
                    self.shaker.set_tone_volume(float(event.text)/100.0)
                if (event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == '#seq_path_input'):
                    self.path = event.text
                    self.shaker.load_tone_sequence(self.path)
                
                
                if (event.type == pygame_gui.UI_BUTTON_PRESSED):
                    #print('button pressed')
                    if (event.ui_element == self.button_play):
                        print('Play Pressed')
                        self.shaker.play_tone()
                
                    if (event.ui_element == self.button_pause):
                        print('Pause Pressed')
                        self.shaker.pause_tone()
                    
                    if (event.ui_element == self.button_play_seq):
                        print('Play Sequence Pressed')
                        self.shaker.play_sequence()
                
                
                self.ui_manager.process_events(event)
            if self.get_serial_input:
                self.update_serial_monitor(time_delta)
            self.ui_manager.update( time_delta )
            self.plot.update( time_delta )
            self.ui_manager.draw_ui(self.screen)
            pygame.display.update()
        
        #Done! Time to quit.
        pygame.quit()
        

    def update_serial_monitor(self, time_delta):
        self.total_time += time_delta

        if self.serial_monitor.buff_is_ready():
            data = self.serial_monitor.get_buffer()
            self.plot.add_point('ax', self.total_time, data[0][0])
            self.plot.add_point('ay', self.total_time, data[0][1])
            self.plot.add_point('az', self.total_time, data[0][2])

    def setup_ui(self):
        self.screen = self.window.set_mode([WIDTH, HEIGHT])
        self.screen.fill("white")
        self.window.set_caption('Harris Lab Shaker Control')
        self.clock = pygame.time.Clock()
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