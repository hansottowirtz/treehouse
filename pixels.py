# coding=utf-8

import recorder
import threading
import time
import signal
import sys
import numpy as np

has_gui = '-gui' in sys.argv
has_cli = '-cli' in sys.argv
has_leds = '-leds' in sys.argv

if has_leds:
    from neopixel import *

    LED_COUNT      = 283     # Number of LED pixels.
    LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
    LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
    LED_BRIGHTNESS = 100     # Set to 0 for darkest and 255 for brightest
    LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

if has_gui:
    import matplotlib
    matplotlib.use('TkAgg')
    import matplotlib.pyplot as plt

class Pixels:
    def __init__(self):
        self.stop = False
        self.first_time = True
        self.data_to_plot1_name = 'my_fft_data'
        self.data_to_plot2_name = None
        self.data = {}

        self.vol = 0

    def start(self):
        if __name__ == '__main__':
            signal.signal(signal.SIGINT, self.close) # on KeyboardInterrupt etc.

        if has_leds:
            try:
                os.rename('/etc/foo', '/etc/bar')
            except IOError as e:
                if (e[0] == errno.EPERM):
                   print >> sys.stderr, "You need root permissions to use the leds!"
                   sys.exit(1)

            self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
            self.strip.begin()
            self.strip.setPixelColor(1, Color(0, 255, 0))
            self.strip.show()

        self.recorder = recorder.Recorder()
        self.recorder.setup()
        self.recorder.changeable['reference_db'] = 3
        self.recorder.verbose = False

        self.frame_counter = 0
        self.bass_buffer = []
        self.mid_buffer = []
        self.treble_buffer = []

        thread = threading.Thread(target=self.recorder.record)
        thread.start()

        self.recorder.request_frame(self.on_frame)

        if has_gui:
            self.start_gui()

    def on_frame(self, response):
        if not self.stop:
            # I combine the logarithmic power with the real power, without a good explanation
            self.data[self.data_to_plot1_name] = my_fft_data = ((np.log10(response['positive_fft_data']/self.recorder.changeable['reference_db']).clip(0))/3)*response['positive_fft_data']/10

            # Bass is in range 20-300 Hz, mid is between 300-1250 Hz, and treble is between 1250-14000 Hz
            response['bass'] = np.average(my_fft_data[1:7])*self.recorder.changeable['bass_weight']*self.recorder.changeable['multiplier']
            response['mid'] = np.average(my_fft_data[7:29])*self.recorder.changeable['mid_weight']*self.recorder.changeable['multiplier']
            response['treble'] = np.average(my_fft_data[29:325])*self.recorder.changeable['treble_weight']*self.recorder.changeable['multiplier']

            if self.frame_counter % 100 == 0 and self.frame_counter != 0: # About every fourth of a second
                self.draw_dots(np.average(self.bass_buffer), np.average(self.mid_buffer), np.average(self.treble_buffer), response['rms'])
                self.bass_buffer = []
                self.mid_buffer = []
                self.treble_buffer = []
                # print pixels['frame_counter'] #np.average(pixels['bass_buffer'])

            self.bass_buffer.append(response['bass'])
            self.mid_buffer.append(response['mid'])
            self.treble_buffer.append(response['treble'])

            self.frame_counter = self.frame_counter + 1

            self.recorder.request_frame(self.on_frame)

    def draw_dots(self, bass, mid, treble, rms):
        if has_cli:
            dot = u'-'
            print dot*int(bass/100)
            print dot*int(mid/100)
            print dot*int(treble/100)
            print

        if has_leds:
            self.vol = int(rms/100)
            thread = threading.Thread(target=self.set_leds)
            thread.start()


    def close(self, *args, **kwargs):
        print 'Closing plot and recorder'
        self.stop = True
        self.recorder.close()

    if has_gui:
        def start_gui(self):
            try:
                time.sleep(0.5)
                self.fig = plt.figure()
                ax = self.fig.add_subplot(111)

                # some X and Y data
                y1 = self.data[self.data_to_plot1_name]
                if self.data_to_plot2_name:
                    y2 = self.data[self.data_to_plot2_name]

                x = np.arange(0, len(y1)*(self.recorder.rate/self.recorder.buffer_size), (self.recorder.rate/self.recorder.buffer_size))

                # ax.set_xscale('log')
                self.li1, = ax.plot(x, y1, 'b-')
                if self.data_to_plot2_name:
                    self.li2, = ax.plot(x, y2, 'r-')
                plt.ylim([-100, 4000])
                plt.xlim([0, 14000])

                # draw and show it
                self.fig.canvas.draw()
                plt.ylabel('Power')
                plt.xlabel('Frequency (Hz)')
                plt.show(block=False)

                time.sleep(1)

                while True and not self.stop:
                    self.draw_plot()
                    time.sleep(0.05)

            except:
                self.close()
                raise

        def draw_plot(self):
            y1 = self.data[self.data_to_plot1_name]
            self.li1.set_ydata(y1)
            if self.data_to_plot2_name:
                y2 = self.data[self.data_to_plot2_name]
                self.li2.set_ydata(y2)

            self.fig.canvas.draw()

    if has_leds:
        def set_leds(self):
            for i in range(self.strip.numPixels()):
                if i < self.vol:
                    self.strip.setPixelColor(i, Color(0, 153, 204))
                else:
                    self.strip.setPixelColor(i, Color(0, 0, 0))
            self.strip.show()


if __name__ == '__main__':
    pixel = None
    try:
        pixel = Pixels()
        signal.signal(signal.SIGINT, pixel.close) # on KeyboardInterrupt etc.
        pixel.start()
    except KeyboardInterrupt:
        pixel.close()
