# copied from https://github.com/WardBenjamin/SimplexNoise.git


import random
import numpy
import math


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

    def calc2D_smooth(self, width: int, height: int, scale: float, smooth_count: int):
        values = numpy.array(self.calc2D(width, height, scale))
        kernel = numpy.array([1, 2, 1]) / 4
        for i in range(smooth_count):
            values = numpy.apply_along_axis(lambda x: numpy.convolve(x, kernel, mode='same'), 0, values)
            values = numpy.apply_along_axis(lambda x: numpy.convolve(x, kernel, mode='same'), 1, values)
        return list(values)

    def calc2D_corners(self, width: int, height: int, scale: float):
        values = numpy.zeros(width * height).reshape((width, height))
        for i in range(height):
            for j in range(width):
                values[i, j] = self.smooth_noise(i * scale, j * scale) * 128 + 128
                print(values[i][j])
        return list(values)

    def interpolate(self, x, y):
        int_x = int(x)
        fraction_x = x - int_x
        int_y = int(y)
        fraction_y = y - int_y
        v1 = self.smooth_noise(int_x, int_y)
        v2 = self.smooth_noise(int_x + 1, int_y)
        v3 = self.smooth_noise(int_x, int_y + 1)
        v4 = self.smooth_noise(int_x + 1, int_y + 1)
        i1 = self.cosine_interpolate(v1, v2, fraction_x)
        i2 = self.cosine_interpolate(v3, v4, fraction_x)
        return self.cosine_interpolate(i1, i2, fraction_y) * 100

    def smooth_noise(self, x, y):
        corners = (self.generate(x - 1, y - 1) + self.generate(x + 1, y - 1) + self.generate(x - 1,
                                                                                             y + 1) + self.generate(
            x + 1, y + 1)) / 16
        sides = (self.generate(x - 1, y) + self.generate(x + 1, y) + self.generate(x, y + 1) + self.generate(x,
                                                                                                             y - 1)) / 8
        center = self.generate(x, y) / 4
        return corners + sides + center

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

    @staticmethod
    def cosine_interpolate(a, b, x):
        ft = x * math.pi
        f = (1 - math.cos(ft)) * 0.5
        return a * (a - f) + b * f

    @staticmethod
    def update_perm():
        """** description **
        sets perm_original new values"""
        Noise.perm_original = [random.randint(0, 255) for _ in range(512)]
