import cv2

# Functions to test
from img_combiner import pixel_constraint  # pixel_constraint(hlow, hhigh, slow, shigh, vlow, vhigh)
from img_combiner import generator_from_image  # generator_from_image(bgr_list)
from img_combiner import combine_images  # combine_images(hsv_list, condition, gen1, gen2)

from img_to_list import cvimg_to_list  # cvimg_to_list(img)

plane_img = cv2.imread("plane.jpg")
plane_hsv_img = cv2.cvtColor(plane_img, cv2.COLOR_BGR2HSV)
plane_bgr_list = cvimg_to_list(plane_img)
plane_list = cvimg_to_list(plane_hsv_img)

gradient_img = cv2.imread("gradient.jpg")
gradient_list = cvimg_to_list(gradient_img)

avatar_img = cv2.imread("avatar.png")
avatar_list = cvimg_to_list(avatar_img)


def test_pixel_constraint(arg=plane_list[0]):
    is_sky = pixel_constraint(100, 150, 50, 200, 100, 255)
    assert is_sky(arg) == 1  # Check motivering.txt (1)
    print("Assertion for pixel_constraint is correct")  # Doesn't execute if AssertionError is raised
    print(" - The first pixel returns a 1, because it is part of the sky in plane.jpg", "\n")


def test_generator_from_image(index=0):
    generator = generator_from_image(gradient_list)
    assert generator(index) == (1, 1, 1)  # Check motivering.txt (2)
    print("Assertion for generator_from_image is correct")  # Doesn't execute if AssertionError is raised
    print(" - The first pixel of gradient.jpg has the bgr value (1,1,1)", "\n")


def test_combine_images(gen2_list=gradient_list):
    is_sky = pixel_constraint(100, 150, 50, 200, 100, 255)
    plane_gen = generator_from_image(plane_bgr_list)
    gradient_gen = generator_from_image(gen2_list)

    combined_img = combine_images(plane_list, is_sky, plane_gen, gradient_gen)
    combined_gen = generator_from_image(combined_img)
    assert combined_gen(0) == gradient_gen(0)  # Check motivering.txt (3.a)
    assert combined_gen(plane_img.shape[0] * plane_img.shape[1] - 1) == plane_gen(
        plane_img.shape[0] * plane_img.shape[1] - 1)  # Check motivering.txt (3.b)
    print("Assertion for combine_images is correct")  # Doesn't execute if AssertionError is raised
    print(" - plane.jpg and gradient.jpg can be combined, because they are the same size", "\n")


def test_functions():
    print("[TESTING FUNCTION ASSERTIONS]")
    test_pixel_constraint()
    test_generator_from_image()
    test_combine_images()


def test_function_exceptions():
    print("[TESTING FUNCTION EXCEPTIONS]")
    try:
        print("Trying to insert an int into pixel_constraints returned function")
        test_pixel_constraint(1)
    except:
        print(" - The function returned requires a tuple, not an int as an argument", "\n")

    try:
        print("Trying to insert an int greater than the pixel amount in generator_from_image")
        test_generator_from_image(10 ** 100)
    except:
        print(" - The index 1 googol is non-existant", "\n")

    try:
        print("Trying to combine images of different sizes in combine_images")
        test_combine_images(avatar_list)
    except:
        print(" - Two images of different sizes cannot be combined", "\n")


test_functions()
print()
test_function_exceptions()
