# copied from https://github.com/WardBenjamin/SimplexNoise.git


import random
import numpy


def FastFloor(x: float):
    return int(x) if x > 0 else int(x) - 1


def Mod(x: int, m: int):
    a = x % m
    return a + m if a < 0 else a


def Grad(perm_hash: int, x: float, y: float):
    h = perm_hash & 7
    u = x if h < 4 else y
    v = y if h < 4 else x
    return (-u if h & 1 != 0 else u) + (-2 * v if h & 2 != 0 else 2 * v)


class Noise:
    perm_original = [random.randint(0, 255) for i in range(512)]

    def calc2D(self, width: int, height: int, scale: float):
        values = numpy.zeros(width * height).reshape((width, height))
        for i in range(width):
            for j in range(height):
                values[i, j] = self.generate(i * scale, j * scale) * 128 + 128
        return list(values)

    @staticmethod
    def generate(x: float, y: float):
        F2 = 0.366025403
        G2 = 0.211324865

        s = (x + y) * F2
        xs = x + s
        ys = y + s
        i = FastFloor(xs)
        j = FastFloor(ys)

        t = (i + j) * G2
        X0 = i - t
        Y0 = j - t
        x0 = x - X0
        y0 = y - Y0

        if x0 > y0:
            i1 = 1
            j1 = 0
        else:
            i1 = 0
            j1 = 1

        x1 = x0 - i1 + G2
        y1 = y0 - j1 + G2
        x2 = x0 - 1.0 + 2.0 * G2
        y2 = y0 - 1.0 + 2.0 * G2

        ii = Mod(i, 256)
        jj = Mod(j, 256)

        t0 = 0.5 - x0 * x0 - y0 * y0
        if t0 < 0.0:
            n0 = 0.0
        else:
            t0 *= t0
            n0 = t0 * t0 * Grad(Noise.perm_original[ii + Noise.perm_original[jj]], x0, y0)

        t1 = 0.5 - x1 * x1 - y1 * y1
        if t1 < 0.0:
            n1 = 0.0
        else:
            t1 *= t1
            n1 = t1 * t1 * Grad(Noise.perm_original[ii + i1 + Noise.perm_original[jj + j1]], x1, y1)

        t2 = 0.5 - x2 * x2 - y2 * y2
        if t2 < 0.0:
            n2 = 0.0
        else:
            t2 *= t2
            n2 = t2 * t2 * Grad(Noise.perm_original[ii + 1 + Noise.perm_original[jj + 1]], x2, y2)

        return 40.0 * (n0 + n1 + n2)
