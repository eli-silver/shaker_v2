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
    """
    Top level object. Runs the main loop for plotting and getting new data from accelerometers.
    Shaker contains: 
        -Tone: sound that is played through the shaker
        -Window: the system window with layout and GUI elements
        -Plot: pixel based canvas within Window, used to plot data
        -Serial_Monitor: real time communication with microcontroller to relay accel data
        -Filter: data processing functions for real time accel data
    """
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
        ### update state of displayed information, runs 120 times per second ###
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

                # get info from text entry boxes
                if (event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == '#frequency_input'):
                    self.set_tone_frequency(float(event.text))    
                if (event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == '#volume_input'):
                    self.set_tone_volume(float(event.text)/100.0)
                if (event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == '#seq_path_input'):
                    self.path = event.text
                    self.load_tone_sequence(self.path)

                # Change state of tone being played based on UI button click
                if (event.type == pygame_gui.UI_BUTTON_PRESSED):
                    if (event.ui_element == self.window.button_play):
                        print('Play Pressed')
                        self.play_tone()
                    if (event.ui_element == self.window.button_pause):
                        print('Pause Pressed')
                        self.pause_tone()
                    
                    if (event.ui_element == self.window.button_play_seq):
                        print('Play Sequence Pressed')
                        self.play_sequence()
            # If we expect to have a microcotroller connected, get new serial data
            if self.run_serial_monitor:
                self.update_serial_monitor(time_delta)

            # Update display with new info
            self.window_ui_manager.update( time_delta )
            self.plot.update( time_delta )
            self.window_ui_manager.draw_ui(self.window_screen)
            pygame.display.update() 
        # when (x) is clicked, exit update loop
        pygame.quit()

    
    
    
    
    def update_serial_monitor(self, time_delta):
        # get most recent serial data
        self.total_time += time_delta

        if self.serial_monitor.buff_is_ready():
            # only plotting the last received data point. Data array can have many points
            data = self.serial_monitor.get_buffer()
            self.plot.add_point('ax', self.total_time, data[0][0])
            self.plot.add_point('ay', self.total_time, data[0][1])
            self.plot.add_point('az', self.total_time, data[0][2])
    
    
    def init_tone(self):
        # define a starting tone, init tone variables
        self.tone = self.load_tone(220,0.25,speaker=None)
        self.tone_running = False
        self.tone_sequence_running = False
        self.tone_sequence_path = None
        self.tone_sequence = None
        self.fade_ms = 0 # volume fade in/out, input to pygame audio library
        self.speaker = 'r' # play out of only one speaker channel 

    def init_window(self):
        # create system window and init window variables
        self.window = Window(self.display)
        self.window_plot_area = self.window.get_plot_area()
        self.window_display = self.window.get_display()
        self.window_screen = self.window.get_screen()
        self.window_ui_manager = self.window.get_ui_manager()

    def init_plot(self):
        # instantiate Plot object, including window to plot in and plot coordinates within window
        self.plot = Plot(self.window_screen, *self.window_plot_area)

    def init_serial_monitor(self):
        # instantiate serial monitor. Pass in info to decode data. Must match values expected from microcontroller
        self.serial_monitor = Serial_Monitor(num_data_bytes=2, num_traces = 4)

    def init_filter(self):
        # set up filtering of incoming data
        pass

    def exit(self):
        # end of program code
        print('THANKS FOR SHAKING')
    
    def load_tone(self, freq, amp, speaker=None, fade_ms=0):
        # create a new Tone object. Wrapper function to make things consistent 
        return Tone(freq, amp, speaker, fade_ms)
        
    def play_tone(self, tone=None):
        # If a tone can be played, play it. Will play currently loaded tone by default unles tone arg is set.
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
        # Play a sequence of tones from a tone file. Sequence is played in a separate thread.
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
        # Pause current tone. Cannot pause a tone sequence 
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
        # change frequency of currently set tone. If tone is playing, changes to frequency will stop curr
        # tone and create a new one with new frequency. Volume of new tone set to vol of old tone
        volume = self.tone.get_volume()
        next_tone = self.load_tone(frequency, volume, speaker=None, fade_ms=0)
        if self.tone_running:    
            self.pause_tone()
            self.tone = next_tone
            self.play_tone()
        else:
            self.tone=next_tone
        
    def set_tone_volume(self, volume, speaker=None, fade_ms=0):
        # Set volume of tone. This does not create a new tone, delay / jump in output *should* happen.
        if(volume >1):
            volume=1
        if(volume < 0):
            volume=0
        self.tone.set_volume(volume)
            
    def load_tone_sequence(self,path):
        # load in a new sequence of tones from a file. Must be in correct csv format
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
        # begin playing tone sequence
        print('begin playing tone sequence')
        self.tone_sequence_running = True
        self.tone_running = True
        
        for tone in self.tone_sequence:
            tone[0].play_cycles(tone[2])
            sleep(tone[1])        
            
        self.tone_sequence_running = False
        self.tone_running = False
        print('tone sequence complete')

        
