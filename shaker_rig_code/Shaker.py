#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 14:45:10 2022

@author: eli
"""

from Tone import Tone
import pygame
from Window import Window
from time import sleep
import threading

bits = 16
sample_rate = 44100
#pygame.mixer.pre_init(sample_rate,bits)


class Shaker:
    
    def __init__(self):
        self.game = pygame.init()
        pygame.mixer.init(sample_rate,bits)
        self.tone = self.load_tone(200,0.25,speaker=None)
        self.tone_list = []
        self.tone_running = False
        self.tone_sequence_running = False
        self.tone_sequence_path = None
        self.tone_sequence = None
        self.fade_ms = 0
        self.speaker = 'r'
        
        self.window = Window(self)

        

    def end_game(self):
        print('GAME OVER')
    
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
        amplitude = self.tone.get_amplitude()
        next_tone = self.load_tone(frequency, amplitude, speaker=None, fade_ms=0)
        if self.tone_running:    
            self.pause_tone()
            self.tone = next_tone
            self.play_tone()
        else:
            self.tone=next_tone
        
    def set_tone_amplitude(self, amplitude, speaker=None, fade_ms=0):
        if(amplitude >1):
            amplitude=1
        if(amplitude < 0):
            amplitude=0
        frequency = self.tone.get_frequency()
        next_tone = self.load_tone(frequency, amplitude, speaker=None, fade_ms=0)
        if self.tone_running:
            self.pause_tone()
            self.tone=next_tone
            self.play_tone()
        else:
            self.tone=next_tone
        
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