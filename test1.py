import cv2
import cvlib
import img_to_list as a1
import img_combiner as b2


def gradient_condition(bgrtuple):
    """Takes in a pixel and assumes it's greyscaled, then it returns a value from 0-1 based on how white the pixel is"""
    return bgrtuple[2] / 255


def test_code():
    plane_img = cv2.imread("plane.jpg")
    flower_img = cv2.imread("flowers.jpg")
    gradient_img = cv2.imread("gradient.jpg")

    gradient_hsv = a1.cvimg_to_list(cv2.cvtColor(gradient_img, cv2.COLOR_BGR2HSV))
    flower_bgr = a1.cvimg_to_list(flower_img)
    plane_bgr = a1.cvimg_to_list(plane_img)

    flower_gen = b2.generator_from_image(flower_bgr)
    plane_gen = b2.generator_from_image(plane_bgr)

    combined_bgr = b2.combine_images(gradient_hsv, gradient_condition, flower_gen, plane_gen)
    combined_img = cvlib.rgblist_to_cvimg(combined_bgr, gradient_img.shape[0], gradient_img.shape[1])

    cv2.imshow('CombinedFinal Image', combined_img)
    cv2.waitKey(0)
