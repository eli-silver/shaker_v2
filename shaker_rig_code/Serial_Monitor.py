from threading import Thread
import serial
import struct
import copy
import numpy as np
import time

class Serial_monitor:
    def __init__(self,serial_port='/dev/ttyACM1',serial_baud=2000000, num_data_bytes = 2, num_traces = 1, buff_len = 300):
        self.port = serial_port
        self.baud = serial_baud
        self.num_data_bytes = num_data_bytes
        self.num_traces = num_traces
        self.buff_len = buff_len
        self.raw_data = bytearray(num_data_bytes * num_traces)
        self.data_type = None
        if num_data_bytes == 2:
            self.data_type = 'h'
        elif num_data_bytes == 4:
            self.data_type = 'f'
        self.data_buff = np.zeros((self.buff_len, self.num_traces))
        self.prev_data_buff = np.zeros((self.buff_len,self.num_traces))
        self.data_buff_index = 0
        self.is_run = True
        self.is_receiving = False
        self.thread = None
        self.plot_timer = 0
        self.prev_plot_timer = 0

        print('Trying to connect to: ' + str(serial_port) + ' at ' + str(serial_baud) + ' BAUD.')
        try:
            self.serial_connection = serial.Serial(serial_port, serial_baud, timeout=4)
            print('Connected to ' + str(serial_port) + ' at ' + str(serial_baud) + ' BAUD.')
        except:
            print("Failed to connect with " + str(serial_port) + ' at ' + str(serial_baud) + ' BAUD.')

    def serial_input_background_init(self):
        if self.thread == None:
            self.thread = Thread(target = self.background_thread)
            self.thread.start()
            while self.is_receiving != True:
                time.sleep(0.1) # wait until background thread starts receiving data

    def background_thread(self):
        time.sleep(1)
        self.serial_connection.reset_input_buffer()
        while( self.is_run):
            self.serial_connection.readinto(self.raw_data)
            self.is_receiving = True
            print('read data from port')


    def close(self):
        self.is_run = False
        self.thread.join()
        self.serial_connection.close()
        print('Disconnected....')