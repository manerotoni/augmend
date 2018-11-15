"""

mweigert@mpi-cbg.de
"""
from __future__ import print_function, unicode_literals, absolute_import, division
import numpy as np
from augmend import Augmend, Elastic, FlipRot, Identity, AdditiveNoise, CutOut

if __name__ == '__main__':
    X = np.zeros((100,) * 2, np.float32)

    X[::8] = 50
    X[:, ::8] = 50
    X[10:50, 10:80] = 100
    X[50:80, 10:30] = 150

    Y = (X * (X > 70)).astype(np.uint16)

    Z = 0 * Y
    Z[30:40, 40:90] = 20

    aug = Augmend()
    aug.add([FlipRot() + Elastic(),
             FlipRot() + Elastic(order=0),
             Identity()])

    aug.add([AdditiveNoise(sigma=20) + CutOut(width=20),
             Identity(),
             Identity()])


    import matplotlib
    import matplotlib.pyplot as plt

    r = np.random.RandomState(31)
    cols = r.uniform(.3, 1., (200, 3))
    cols[0] *= 0
    cmap_rand = matplotlib.colors.ListedColormap(cols)

    fig = plt.figure(num=1)
    fig.clf()
    axs = fig.subplots(3, 6)

    for i,(ax1, ax2, ax3) in enumerate(zip(*axs)):
        X2, Y2, Z2 = aug([X, Y,Z])
        ax1.imshow(X2, cmap="gray")
        ax1.axis("off")
        ax1.set_title("X_%s"%i, fontsize = 6)
        ax2.imshow(Y2, cmap=cmap_rand, vmin = 0, vmax = 255)
        ax2.axis("off")
        ax2.set_title("Y_%s" % i, fontsize=6)
        ax3.imshow(Z2, cmap=cmap_rand, vmin = 0, vmax = 255)
        ax3.axis("off")
        ax3.set_title("Z_%s" % i, fontsize=6)

    plt.show()
