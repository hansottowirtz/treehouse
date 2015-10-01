# coding=utf-8

import numpy
import pyaudio
import audioop
import threading
import time

CHUNK = 1024
CHANNELS = 2
RATE = 44100

class Recorder:
    # General stuff

    def __init__(self):
        self.rate = RATE
        self.buffer_size = CHUNK
        self.channels = CHANNELS

        self.frame_request_buffer = []

        self.verbose = False

        self.stopping = False
        self.loop_stopped = False
        self.stream_stopped = False

        self.changeable = {'bass_weight': 1, 'mid_weight': 10, 'treble_weight': 100, 'multiplier': 1, 'reference_db': 1}

    def setup(self):
        self.seconds_per_point = 1.0/self.rate

        self.pa = pyaudio.PyAudio()

        self.open_stream()

    def open_stream(self):
        print 'Opening stream'
        self.stream = self.pa.open(format = pyaudio.paInt16, channels = self.channels, rate = self.rate, input = True, frames_per_buffer = self.buffer_size)

    def close(self):
        print 'Stopping recorder'
        self.stopping = True

        for i in range(0, 15):
            if not self.loop_stopped:
                time.sleep(0.1)
            else:
                break

        if not self.loop_stopped:
            print 'Loop didn\'t stop'


        time.sleep(0.1)
        print 'Stopping stream'
        self.stream.stop_stream()

        print 'Closing stream'
        self.stream.close()

        print 'Terminating PyAudio'
        self.pa.terminate()

        self.stream_stopped = True

    # Recording

    def record(self):
        while True:
            if self.stopping:
                self.loop_stopped = True
                break
            else:
                raw_data = self.stream.read(self.buffer_size)

                wave_data = numpy.fromstring(raw_data, dtype = numpy.int16)
                rms = audioop.rms(wave_data, 2)

                fft_function_data = numpy.fft.fft(wave_data).flatten()
                if self.verbose: print 'fft_function_data %s' % fft_function_data[512]

                # The FFT function creates a symmetrical function.
                # If you compare them it might not be exactly mirrored but that's
                # because of approximations. Mathematically, it"s symmetrical.
                # See https://www.youtube.com/watch?v=dM1y6ZfQkDU
                left, right = numpy.split(fft_function_data, 2)
                complex_fft_data = left
                if self.verbose: print 'complex_fft_data %s' % complex_fft_data[512]


                # # Here, we add the imaginary and the real data components to each other.
                # # I have no idea why, but it sounded great here:
                # # See http://www.swharden.com/blog/2010-06-23-insights-into-ffts-imaginary-numbers-and-accurate-spectrographs/
                # real_plus_imag_fft_data = numpy.sqrt(complex_fft_data.imag**2+complex_fft_data.real**2)


                # As an FFT array has complex numbers, with the magnitude as its real component,
                # and the phase as its imaginary component, we just take the real components.
                real_fft_data = complex_fft_data.real
                if self.verbose: print 'real_fft_data %s' % real_fft_data[512]

                positive_fft_data = numpy.abs(real_fft_data)
                if self.verbose: print 'positive_fft_data %s' % positive_fft_data[512]

                # This will be returned to frame_request
                response = {
                    'rms': rms,
                    'wave_data': wave_data,
                    'fft_function_data': fft_function_data,
                    'complex_fft_data': complex_fft_data,
                    'real_fft_data': real_fft_data,
                    'positive_fft_data': positive_fft_data,
                    #'decibel_fft_data': decibel_fft_data,
                }

                frame_request_buffer_clone = list(self.frame_request_buffer)
                self.frame_request_buffer = []
                for fn in frame_request_buffer_clone:
                    fn(response)

    def request_frame(self, fn):
        self.frame_request_buffer.append(fn)
