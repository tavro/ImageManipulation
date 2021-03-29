import cv2
import numpy
import math


def calculate_gaussian(x, y):
    """Calculates gaussian value based on x,y"""
    s = 4.5
    e_exponent = -(x ** 2 + y ** 2) / (2 * s ** 2)
    denominator = (2 * math.pi * s ** 2)
    return -math.e ** e_exponent / denominator


def calculate_centered_gaussian(x, y, N):
    """Calculates gaussian value when x,y are remapped by floored N/2"""
    remapped_x = x - math.floor(N / 2)
    remapped_y = y - math.floor(N / 2)

    if (remapped_x, remapped_y) == (0, 0):
        return 1.5
    else:
        return calculate_gaussian(remapped_x, remapped_y)


def unsharp_mask(N):
    """Returns a square list of size N, which can be used when sharpening an image"""
    list2D = [[calculate_centered_gaussian(x, y, N) for x in range(N)] for y in range(N)]

    return list2D


def test_code():
    print(unsharp_mask(3))
