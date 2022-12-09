#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 17:45:20 2022

@author: eli
"""

import math        #import needed modules
import pyaudio     #sudo apt-get install python-pyaudioPyAudio = pyaudio.PyAudio     #initialize pyaudio
BITRATE = 44100     #number of frames per second/frameset.
FREQUENCY = 180     #Hz, waves per second, 261.63=C4-note.
LENGTH = 20   #seconds to play soundif FREQUENCY > BITRATE:
#BITRATE = 44100
NUMBEROFFRAMES = int(BITRATE * LENGTH)
RESTFRAMES = NUMBEROFFRAMES % BITRATE
WAVEDATA = ''
MAX_AMPLITUDE = 127
volume = .5 # value from 0.0 to 1.0
amp_int = math.floor(MAX_AMPLITUDE*volume)
print(amp_int)
#generating waves
for x in range(NUMBEROFFRAMES):
     WAVEDATA = WAVEDATA+chr(int(math.sin(x/((BITRATE/FREQUENCY)/math.pi))*amp_int+128))
for x in range(RESTFRAMES):
    WAVEDATA = WAVEDATA+chr(128)
#print(WAVEDATA)
p = pyaudio.PyAudio()
stream = p.open(format = p.get_format_from_width(1),channels =2,rate = BITRATE,output = True)
stream.write(WAVEDATA)
stream.stop_stream()
stream.close()
p.terminate()