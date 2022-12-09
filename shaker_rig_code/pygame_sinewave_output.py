import pygame
import numpy
import math
from time import sleep

pygame.init()

bits = 16
sample_rate = 44100

pygame.mixer.pre_init(sample_rate,bits)


def sine_t(A, t, f):
    return int(round( A * math.sine( 2 * math.pi * f * t )))

class Tone:
    
    def sine(f, duration, speaker=None):
        num_samples = int(round( duration * sample_rate )) 
        sound_buff = numpy.zeros((num_samples,2), dtype=numpy.int16)
        amplitude = 2 ** (bits -1) -1
        
        for sample_num in range(num_samples):
            t = float(sample_num)/sample_rate
            
            sine = sine_t(amplitude, t, f)
            
            if speaker == 'r':
                sound_buff[sample_num][1] = sine
            if speaker == 'l':
                sound_buff[sample_num][0] = sine
            else:
                sound_buff[sample_num][1] = sine
                sound_buff[sample_num][0] = sine
                
                
        sound = pygame.sndarray.make_sound(sound_buff)
        sound.play(loops = 1, maxtime = int(duration * 1000))
        sleep(duration)
        
#def main():
#    Tone.sine_init(220, 2)
    
#if __name__ == '__main__':
#    main()

