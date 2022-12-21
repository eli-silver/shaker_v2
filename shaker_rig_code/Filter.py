import numpy as np
from scipy import fft, signal



class Filter:
    def __init__(self, freq, sample_rate, buff_len, num_traces, trigger_trace, threshold):
        self.freq = freq
        self.sample_rate = sample_rate
        self.buff_len = buff_len
        self.num_traces = num_traces
        self.trigger_trace = trigger_trace
        self.threshold = threshold

        self.nyquist_freq = freq / 2
        self.cutoff_multiplier = 5
        self.input_buff = np.zeros((num_traces, buff_len))
        self.output_buff = np.zeros((num_traces, buff_len))

        self.init_filter(self.freq, self.freq * self.cutoff_multiplier)


    def init_filter (self, freq, cutoff_freq):
        self.cutoff_freq = cutoff_freq
        Wn = self.cutoff_freq / self.nyquist_freq
        self.filter_arg_b, self.filter_arg_a = signal.butter( 3, Wn, 'lowpass')


    def set_freq(self, freq):
        self.freq = freq
        self.init_filter(self.freq, self.freq * self.cutoff_multiplier)


    def apply_filter(self, data_buff):
        self.input_buff = np.asarray(data_buff)

        for i in len(self.input_buff):
            self.output_buff[i] = signal.filtfilt(self.filter_arg_b, self.filter_arg_a, self.input_buff[i])
        return self.output_buff


    def find_rising_edges(self):
        pass