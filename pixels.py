# coding=utf-8

import recorder
import threading
import time
import signal
import sys
import numpy as np

# from neopixel import *

has_gui = '-gui' in sys.argv
has_cli = '-cli' in sys.argv

if has_gui:
    import matplotlib
    matplotlib.use('TkAgg')
    import matplotlib.pyplot as plt

pixels = {'stop': False, 'first_time': True}

PLOTTED_DATA = 'positive_fft_data'
PLOTTED_DATA_2 = 'decibel_fft_data'

r = recorder.Recorder()
r.setup()
r.changeable['reference_db'] = 3
r.verbose = False

# volume_array = np.zeros(shape=(10,3))

pixels['frame_counter'] = 0
pixels['bass_buffer'] = []
pixels['mid_buffer'] = []
pixels['treble_buffer'] = []

def on_frame(response):
    if not pixels['stop']:
        pixels[PLOTTED_DATA] = response['positive_fft_data']/1000
        pixels[PLOTTED_DATA_2] = my_fft_data = ((np.log10(response['positive_fft_data']/r.changeable['reference_db']).clip(0))/3)*response['positive_fft_data']/10
        #
        # Bass is in range 20-300 Hz, mid is between 300-1250 Hz, and treble is between 1250-14000 Hz
        response['bass'] = np.average(my_fft_data[1:7])*r.changeable['bass_weight']*r.changeable['multiplier']
        response['mid'] = np.average(my_fft_data[7:29])*r.changeable['mid_weight']*r.changeable['multiplier']
        response['treble'] = np.average(my_fft_data[29:325])*r.changeable['treble_weight']*r.changeable['multiplier']

        if pixels['frame_counter'] % 5 == 0 and pixels['frame_counter'] != 0: # About every fourth of a second
            draw_dots(np.average(pixels['bass_buffer']), np.average(pixels['mid_buffer']), np.average(pixels['treble_buffer']))
            pixels['bass_buffer'] = []
            pixels['mid_buffer'] = []
            pixels['treble_buffer'] = []
            # print pixels['frame_counter'] #np.average(pixels['bass_buffer'])

        pixels['bass_buffer'].append(response['bass'])
        pixels['mid_buffer'].append(response['mid'])
        pixels['treble_buffer'].append(response['treble'])

        pixels['frame_counter'] = pixels['frame_counter'] + 1
        r.request_frame(on_frame)

r.request_frame(on_frame)

def draw_dots(bass, mid, treble):
    if has_cli:
        dot = u'█'
        # print bass
        # print mid
        # print treble
        print dot*int(bass/100)
        print dot*int(mid/100)
        print dot*int(treble/100)
        print

def close(a = '', b = ''):
    print 'Closing plot and recorder'
    pixels['stop'] = True
    r.close()

signal.signal(signal.SIGINT, close) # on KeyboardInterrupt etc.

t = threading.Thread(target=r.record)
t.start()

print r.rate
print r.buffer_size

if has_gui:
    try:
        def draw_plot():
            y1 = (pixels[PLOTTED_DATA])
            y2 = (pixels[PLOTTED_DATA_2])

            # set the new data
            li1.set_ydata(y1)
            li2.set_ydata(y2)
            fig.canvas.draw()

        time.sleep(0.5)
        fig = plt.figure()
        ax = fig.add_subplot(111)

        # some X and Y data
        y1 = (pixels[PLOTTED_DATA]/100)
        y2 = (pixels[PLOTTED_DATA_2]*100)
        x = np.arange(0, len(y1)*(r.rate/r.buffer_size), (r.rate/r.buffer_size))

        # ax.set_xscale('log')
        li2, = ax.plot(x, y2, 'r-')
        li1, = ax.plot(x, y1, 'b-')
        plt.ylim([-100, 4000])
        plt.xlim([0, 14000])

        # draw and show it
        fig.canvas.draw()
        plt.ylabel('Power')
        plt.xlabel('Frequency (Hz)')
        plt.show(block=False)

        time.sleep(1)

        while True and not pixels['stop']:
            draw_plot()
            time.sleep(0.05)

    except:
        close()
        raise
