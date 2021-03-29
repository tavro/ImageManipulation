import cv2
import cvlib


def cvimg_to_list(img):
    """Returns a list of pixel colors of a given cv2 image"""
    pixels = []
    for x in range(len(img)):
        for y in range(len(img[x])):
            pixel_color = (img[x, y][0], img[x, y][1], img[x, y][2])
            pixels.append(pixel_color)
    return pixels


def test_code():
    img = cv2.imread('avatar.png')
    print(cvimg_to_list(img))
