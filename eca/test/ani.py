# -*- coding: utf-8 -*-
# @Time : 2020/8/22 上午10:36
# @Author : cmk
# @File : ani.py

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from tqdm import tqdm

fig, ax = plt.subplots()


def f(x, y):
    return np.sin(x) + np.cos(y)

x = np.linspace(0, 2 * np.pi, 120)
y = np.linspace(0, 2 * np.pi, 100).reshape(-1, 1)

# ims is a list of lists, each row is a list of artists to draw in the
# current frame; here we are just animating one artist, the image, in
# each frame
import time
st = time.time()
ims = []
im = ax.imshow([[]], animated=True)
for i in tqdm(range(60)):
    x += np.pi / 15.
    y += np.pi / 20.
    # im = ax.imshow(f(x, y), animated=True)
    im.set_data(f(x, y))
    if i == 0:
        ax.imshow(f(x, y))  # show an initial one first
    # plt.savefig("./test/tmp/img_{}.jpg".format(str(i)), dpi=96)
    ims.append([im])
print("s1 : ", time.time() - st)
st = time.time()
# ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True,
#                                 repeat_delay=1000)
ani = animation.FuncAnimation(
    fig, animate, len(y), interval=dt*1000, blit=True)
print("s2:", time.time() - st)
st = time.time()
# ani.save('./test/test_animation.gif', writer='imagemagick')
# from acca.utils import create_gif
# create_gif(img_dir="./test/tmp", save_gif_path="./test/test.gif", duration=0.5)
print("s3:", time.time() - st)
# To save the animation, use e.g.
#
# ani.save("movie.mp4")
#
# or
#
# writer = animation.FFMpegWriter(
#     fps=15, metadata=dict(artist='Me'), bitrate=1800)
# ani.save("movie.mp4", writer=writer)

plt.show()