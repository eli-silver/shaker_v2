import pygame
import numpy
import math
from time import sleep

pygame.init()

bits = 16
sample_rate = 44100

pygame.mixer.pre_init(sample_rate,bits)


def sine_t(A, t, f):
    return int(round( A * math.sin( 2 * math.pi * f * t )))

class Tone:
        
    def __init__(self):
        pass
    
    def sine(self, f, amp, duration, speaker=None, fade = 0):
        
        sound_buff = self.get_sound_buff(f, amp, duration, speaker)
                
        sound = pygame.sndarray.make_sound(sound_buff)
        sound.play(loops = 1, maxtime = int(duration * 1000),fade_ms = fade)
        sleep(duration)
        
        
    def sine_list(self, note_arr):
        for note in note_arr:
            pass
    

    def get_sound_buff(self, freq, amp, duration, speaker=None):
        
        num_samples = int(round( duration * sample_rate )) 
        sound_buff = numpy.zeros((num_samples,2), dtype=numpy.int16)
        amplitude = int(round((2 ** (bits -1) -1) * amp ))
        
        for sample_num in range(num_samples):
            t = float(sample_num)/sample_rate
            
            sine = sine_t(amplitude, t, freq)
            
            if speaker == 'r':
                sound_buff[sample_num][1] = sine
            if speaker == 'l':
                sound_buff[sample_num][0] = sine
            else:
                sound_buff[sample_num][1] = sine
                sound_buff[sample_num][0] = sine
                
        return sound_buff
    

    
    
    
    