#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 14:45:10 2022

@author: eli
"""

from Tone import Tone
from Window import Window
from Plot import Plot
from Serial_Monitor import Serial_Monitor
from Filter import Filter

import pygame
import pygame_gui
from time import sleep
import threading
import serial
import numpy as np

bits = 16
sample_rate = 44100


class Shaker:
    
    def __init__(self):
        self.game = pygame.init()
        pygame.mixer.init(sample_rate,bits)
        self.clock = pygame.time.Clock()
        self.display = pygame.display

        self.init_tone()
        self.init_window()
        self.init_plot()
        self.init_serial_monitor()
        self.run_serial_monitor = False
        if self.run_serial_monitor:
            self.serial_monitor.serial_input_background_init()
        self.init_filter()

        self.total_time = 0

        ### begin update loop ###
        self.run = True
        self.update_loop()


    def update_loop(self):
        while self.run:
            time_delta = self.clock.tick(120)/1000

            for event in pygame.event.get():
                self.window_ui_manager.process_events(event)

                # close window if clicked (x)
                if event.type == pygame.QUIT:
                    self.run = False
                    if self.run_serial_monitor:
                        self.serial_monitor.close()
                    self.exit()

                if (event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == '#frequency_input'):
                    self.set_tone_frequency(float(event.text))    
                if (event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == '#volume_input'):
                    self.set_tone_volume(float(event.text)/100.0)
                if (event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == '#seq_path_input'):
                    self.path = event.text
                    self.load_tone_sequence(self.path)


                if (event.type == pygame_gui.UI_BUTTON_PRESSED):
                    #print('button pressed')
                    if (event.ui_element == self.window.button_play):
                        print('Play Pressed')
                        self.play_tone()
                    if (event.ui_element == self.window.button_pause):
                        print('Pause Pressed')
                        self.pause_tone()
                    
                    if (event.ui_element == self.window.button_play_seq):
                        print('Play Sequence Pressed')
                        self.play_sequence()

            if self.run_serial_monitor:
                self.update_serial_monitor(time_delta)
            self.window_ui_manager.update( time_delta )
            self.plot.update( time_delta )
            self.window_ui_manager.draw_ui(self.window_screen)
            pygame.display.update() 
        pygame.quit()

    
    
    
    
    def update_serial_monitor(self, time_delta):
        self.total_time += time_delta

        if self.serial_monitor.buff_is_ready():
            data = self.serial_monitor.get_buffer()
            self.plot.add_point('ax', self.total_time, data[0][0])
            self.plot.add_point('ay', self.total_time, data[0][1])
            self.plot.add_point('az', self.total_time, data[0][2])
    
    
    def init_tone(self):
        self.tone = self.load_tone(220,0.25,speaker=None)
        self.tone_list = []
        self.tone_running = False
        self.tone_sequence_running = False
        self.tone_sequence_path = None
        self.tone_sequence = None
        self.fade_ms = 0
        self.speaker = 'r'

    def init_window(self):
        self.window = Window(self.display)
        self.window_plot_area = self.window.get_plot_area()
        self.window_display = self.window.get_display()
        self.window_screen = self.window.get_screen()
        self.window_ui_manager = self.window.get_ui_manager()

    def init_plot(self):
        self.plot = Plot(self.window_screen, *self.window_plot_area )

    def init_serial_monitor(self):
        self.serial_monitor = Serial_Monitor(num_data_bytes=2, num_traces = 4)

    def init_filter(self):
        pass

    def exit(self):
        print('THANKS FOR SHAKING')
    
    def load_tone(self, freq, amp, speaker=None, fade_ms=0):
        return Tone(freq, amp, speaker, fade_ms)
        
    def play_tone(self, tone=None):
        if self.tone_sequence_running:
            print('sequence running, cannot play')
        elif self.tone_running:
            print('tone already playing')
        else:
            self.tone_running = True
            if tone==None:
                
                self.tone.play()
            else:
                tone.play()
                
    def play_sequence(self):
        if self.tone_running:
            self.pause_tone()
        elif self.tone_sequence_running:
            print('sequence already running')
        else:
            if self.tone_sequence != None:
                thread = threading.Thread(target = self.play_tone_sequence)
                thread.start()
                return
            else:
                print('sequence not set')
        
    def pause_tone(self,tone=None):
        if self.tone_sequence_running:
            print('sequence running, cannot pause')
            return
        if self.tone_running == False: 
            return
        self.tone_running=False
        if tone==None:
            self.tone.stop()
        else:
            tone.stop()
                            
    def set_tone_frequency(self, frequency):
        volume = self.tone.get_volume()
        next_tone = self.load_tone(frequency, volume, speaker=None, fade_ms=0)
        if self.tone_running:    
            self.pause_tone()
            self.tone = next_tone
            self.play_tone()
        else:
            self.tone=next_tone
        
    def set_tone_volume(self, volume, speaker=None, fade_ms=0):
        if(volume >1):
            volume=1
        if(volume < 0):
            volume=0
        self.tone.set_volume(volume)
        
    def clear_tone_list(self):
        for tone in self.tone_list:
            tone.stop()
            self.tone_list.remove(tone)
            
    def load_tone_sequence(self,path):
        self.tone_sequence = []
        try:
            file = open(path, 'r')
        except:
            print('File Not Found')
            return
        self.path = path
        for line in file:
            # tone parameters from file: freq(0), amp(1), time_sec(2) 
            tone_params = line.split(',')
            tone_params = list(map(float,tone_params)) #convert strings to floats
            num_cycles = int(round(tone_params[0] * tone_params[2]))
            tone = self.load_tone(tone_params[0], tone_params[1]/100)
            self.tone_sequence.append([tone,tone_params[2], num_cycles])
            
    def play_tone_sequence(self):
        print('begin playing tone sequence')
        self.tone_sequence_running = True
        self.tone_running = True
        
        for tone in self.tone_sequence:
            tone[0].play_cycles(tone[2])
            sleep(tone[1])        
            
        self.tone_sequence_running = False
        self.tone_running = False
        print('tone sequence complete')

        
