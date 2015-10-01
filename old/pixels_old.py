def draw_plot():
    y1 = pixels[PLOTTED_DATA][:325]
    # y2 = (pixels[PLOTTED_DATA_2][:325]/20)+50
    # set the new data
    li1.set_ydata(y1)
    # li2.set_ydata(y2)

    fig1.canvas.draw()
    # fig2.canvas.draw()

time.sleep(3)

fig1 = plt.figure(1)
# fig2 = plt.figure(2)
axes1 = fig1.add_subplot(1, 1, 1, ylim = [0, 100], xlim = [0, 14000], ylabel = 'Volume (sort of)', xlabel = 'Frequency (Hz)')
# axes2 = fig2.add_subplot(1, 1, 1)

# # some X and Y data
y1 = pixels[PLOTTED_DATA][:325]
# y2 = (pixels[PLOTTED_DATA_2][:325]/20)+50

x1 = np.arange(0, len(y1)*(r.rate/r.buffer_size), (r.rate/r.buffer_size))
# x2 = np.arange(0, len(y2)*50, 50)

# # ax.set_xscale('log')
li1, = axes1.plot(x1, y1, 'b-')
# li2, = axes2.plot(x2, y2, 'r-')


# plt.ylim([0,100])
# plt.xlim([0,14000])

# # draw and show it
fig1.canvas.draw()
# fig2.canvas.draw()
# fig1.ylabel()
# fig1.xlabel()

plt.show(block = False)
#
time.sleep(0.1)

while True and not pixels['stop']:
    draw_plot()
    time.sleep(0.05)


# older

def draw_plot():
    y = pixels[PLOTTED_DATA]
    y2 = (pixels[PLOTTED_DATA_2][:325]/50)+50

    # set the new data
    li.set_ydata(y[:325]) #, y2[:325])
    li2.set_ydata(y2[:325])
    fig.canvas.draw()

time.sleep(0.5)
fig = plt.figure()
ax = fig.add_subplot(111)
ax2 = fig.add_subplot(111)

# some X and Y data
y = pixels[PLOTTED_DATA][:325]
y2 = (pixels[PLOTTED_DATA_2][:325]/50)+50
x = np.arange(0, len(y)*(r.rate/r.buffer_size), (r.rate/r.buffer_size))
x2 = np.arange(0, len(y2)*50, 50)

# ax.set_xscale('log')
li2, = ax.plot(x2, y2, 'r--')
li, = ax.plot(x, y, 'b-')
plt.ylim([0,100])
plt.xlim([0,14000])

# draw and show it
fig.canvas.draw()
plt.ylabel('Volume (sort of)')
plt.xlabel('Frequency (Hz)')
plt.show(block=False)

time.sleep(0.1)

while True and not pixels['stop']:
    draw_plot()
    time.sleep(0.05)
