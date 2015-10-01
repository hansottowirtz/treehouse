# coding=utf-8

import pyaudio
import numpy
import wave
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as pyplot
import threading
import audioop

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 20
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")

frames = []

print int(RATE / CHUNK * RECORD_SECONDS)
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    # raw_data = stream.read(CHUNK)
    # data = numpy.fromstring(raw_data, dtype = numpy.int16).flatten()
    # fft_data = numpy.fft.fft(data)
    # fft_data = fft_data[100:len(fft_data)-100]
    # data = data[100:len(data)-100]
    #
    # empty_arr = numpy.arange(len(fft_data))

    # real_fft_data = fft_data.real
    # average = int(numpy.average(real_fft_data[900:1100].flatten()))
    # print average

    #if i == 50:

    # left,right=numpy.split(numpy.abs(fft_data), 2)
    # ys=numpy.add(left, right[::-1])
    #
    # i=int((CHUNK/2)/10)
    # ys=ys[:14000]
    # ys=ys/10.0

    # dot = u'⬤'
    # print dot*int((numpy.average(ys[1450/(RATE/CHUNK):1550/(RATE/CHUNK)])/1000))

    raw_data = stream.read(CHUNK)

    data = numpy.fromstring(raw_data, dtype = numpy.int16)
    fft_data = numpy.fft.fft(data)

    left, right = numpy.split(numpy.abs(fft_data), 2)
    ys = numpy.add(left, right[::-1])
    ys = numpy.log10(ys)

    xs = numpy.arange(0, len(ys))*(RATE/CHUNK)
    pyplot.plot(xs, ys, 'b-')
    pyplot.show()

    # frequencies_array = [60, 230, 910, 4000, 14000]
    # for i in range(len(frequencies_array)-1):
    #     print data[frequencies_array[i]:frequencies_array[i+1]]

    # rms = int(numpy.average(fft_data[1400:1600]).real)
    # print rms
    # if i % 10 == 0:
    #     data = numpy.fromstring(raw_data, dtype = numpy.int16)
    #     x = numpy.arange(0, len(data))
    #     pyplot.plot(x, numpy.fft.fft(data))
    #     pyplot.show()
    #     # print '%s %s %s %s %s %s %s %s' % (data[0], data[250], data[500], data[750], data[1000], data[1250], data[1500], data[1750])
    #     # print ''

    # frames.append(data)

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()
#
# wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
# wf.setnchannels(CHANNELS)
# wf.setsampwidth(p.get_sample_size(FORMAT))
# wf.setframerate(RATE)
# wf.writeframes(b''.join(frames))
# wf.close()
