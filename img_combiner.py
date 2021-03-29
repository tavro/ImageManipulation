import cvlib
import cv2
import random
import img_to_list as a1
import effects as a2


def pixel_constraint(hlow, hhigh, slow, shigh, vlow, vhigh):
    """Returns a function which returns a 1 or 0 based on whether or not a pixel fits a given constraint"""

    def fits_constraint(pixel):
        """Returns 1 if the given pixel(HSV) fits the constraints, otherwise 0"""

        if not isinstance(pixel, tuple):
            raise TypeError("The given value of pixel(tuple) is not a tuple!!!")

        fits_h = pixel[0] >= hlow and pixel[0] <= hhigh
        fits_s = pixel[1] >= slow and pixel[1] <= shigh
        fits_v = pixel[2] >= vlow and pixel[2] <= vhigh

        if fits_h and fits_s and fits_v:
            return 1
        else:
            return 0

    return fits_constraint


def test_b1():
    plane_img = cv2.imread("plane.jpg")
    hsv = cv2.cvtColor(plane_img, cv2.COLOR_BGR2HSV)
    hsv_list = a1.cvimg_to_list(hsv)

    is_sky = pixel_constraint(100, 150, 50, 200, 100, 255)
    # Create a list of pixels for each pixel in hsv_list, run through is_sky
    sky_pixel_list = list(map(lambda x: x * 255, map(is_sky, hsv_list)))

    cv2.imshow("sky", cvlib.greyscale_list_to_cvimg(sky_pixel_list, hsv.shape[0], hsv.shape[1]))
    cv2.waitKey(0)


# ----------------------------------------------#

def generator_from_image(bgr_list):
    """Returns a function which returns the color of a pixel at a given index based on an img_list"""

    def generator(i):
        if i >= len(bgr_list):
            raise IndexError("The given index value is greater than the length of the list")

        return bgr_list[i]

    return generator


def test_b2():
    plane_bgr = a1.cvimg_to_list(cv2.imread("plane.jpg"))
    plane_generator = generator_from_image(plane_bgr)
    print(plane_generator(9))


# --------------------------------------------------#

def combine_images(hsv_list, condition, generator1, generator2):
    """Returns an image, as a list, based on two generators and a condition"""
    img_list = []

    for i in range(len(hsv_list)):
        try:
            bgr_from_gen1 = cvlib.multiply_tuple(generator1(i), 1 - condition(hsv_list[i]))
            bgr_from_gen2 = cvlib.multiply_tuple(generator2(i), condition(hsv_list[i]))
        except:
            raise Exception("An error was caused by one of the functions(generator_from_image, pixel_constraint)")

        bgr_to_append = cvlib.add_tuples(bgr_from_gen1, bgr_from_gen2)

        img_list.append(bgr_to_append)

    return img_list


def test_b3():
    plane_img = cv2.imread("plane.jpg")

    sky_detector = pixel_constraint(100, 150, 50, 200, 100, 255)

    plane_hsv = a1.cvimg_to_list(cv2.cvtColor(plane_img, cv2.COLOR_BGR2HSV))  # For detecting sky_pixels
    plane_bgr = a1.cvimg_to_list(plane_img)  # For combining with star_img

    def generate_stars(base_img):
        """Generates an image of a night sky as a list"""
        star_list = []
        for i in base_img:
            star_pixel = random.random() * 255 if random.random() > 0.99 else 0
            star_list.append((star_pixel, star_pixel, star_pixel))
        return star_list

    star_bgr = generate_stars(plane_bgr)

    plane_gen = generator_from_image(plane_bgr)
    star_gen = generator_from_image(star_bgr)

    result = combine_images(plane_hsv, sky_detector, plane_gen, star_gen)
    result_img = cvlib.rgblist_to_cvimg(result, plane_img.shape[0], plane_img.shape[1])

    cv2.imshow("Combined IMG", result_img)
    cv2.waitKey(0)
