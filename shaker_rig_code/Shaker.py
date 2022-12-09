#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 14:45:10 2022

@author: eli
"""

from Tone import Tone
import pygame
from Window import Window

bits = 16
sample_rate = 44100
#pygame.mixer.pre_init(sample_rate,bits)


class Shaker:
    
    def __init__(self):
        self.game = pygame.init()
        pygame.mixer.init(sample_rate,bits)
        self.tone = self.load_tone(300,0.5,speaker=None)
        self.tone_list = []
        self.tone_running = False
        self.window = Window(self)
        

    def end_game(self):
        print('GAME OVER')
    
    def load_tone(self, freq, amp, speaker=None, fade_ms=0):
        return Tone(freq, amp, speaker, fade_ms)
        
    def play_tone(self, tone=None):
        if self.tone_running:
            return
        else:
            self.tone_running = True
            if tone==None:
                
                self.tone.play()
            else:
                tone.play()

        
    def pause_tone(self,tone=None):
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
    
