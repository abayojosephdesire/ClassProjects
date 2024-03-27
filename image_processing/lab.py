#!/usr/bin/env python3

"""
6.101 Lab 1:
Image Processing
"""

import math

from PIL import Image

# NO ADDITIONAL IMPORTS ALLOWED!

# Image pixels are accessed from (0, 0) representing (row, column) respectively
def get_pixel(image, row, col, boundary_behavior=None):
    width = image["width"]
    height = image["height"]
    if (not boundary_behavior) or (0 <= row < height and 0 <= col < width):
        return image["pixels"][(row)*width + col]

    if boundary_behavior == "zero": return 0

    # Used cases to separate extensions on different sides of the square.
    if boundary_behavior == "extend":
        if col <= 0:
            if row <= 0: return get_pixel(image, 0, 0, boundary_behavior)
            if 1 <= row < height-1: return get_pixel(image, row, 0, boundary_behavior)
            if row >= height-1: return get_pixel(image, height-1, 0, boundary_behavior)

        if col < width:
            if row < 0: return get_pixel(image, 0, col, boundary_behavior)
            if row >= height: return get_pixel(image, height-1, col, boundary_behavior)

        if col >= width:
            if row <= 0: return get_pixel(image, 0, width-1, boundary_behavior)
            if 1 <= row < height-1: return get_pixel(image, row, width-1, boundary_behavior)
            if row >= height-1: return get_pixel(image, height-1, width-1, boundary_behavior)

    # Loop through the row and col until you get corresponding numbers falling within
    # the image limits
    if boundary_behavior == "wrap":
        while col < 0: col += width
        while col >= width: col -= width
        while row < 0: row += height
        while row >= height: row -= height
        return get_pixel(image, row, col, boundary_behavior)

# Helper function for returning the value of the kernel at [row, col]
# Since kernel is always a square, we can use the math.sqrt() to find its width
def get_kernel_pixel(kernel, row, col):
    width = int(math.sqrt(len(kernel)))
    return kernel[(row*width) + col]

def get_blur_kernel(kernel_size):
    kernel_pix = 1/ (kernel_size**2)
    return [kernel_pix for _ in range(kernel_size**2)]

def set_pixel(image, row, col, color):
    width = image["width"]
    image["pixels"][(row)*width + col] = color


def apply_per_pixel(image, func):
    result = {
        "height": image["height"],
        "width": image["width"],
        "pixels": image["pixels"][:],
    }
    for row in range(image["height"]):
        for col in range(image["width"]):
            color = get_pixel(image, row, col)
            new_color = func(color)
            set_pixel(result, row, col, new_color)
    return result


def inverted(image):
    return apply_per_pixel(image, lambda color: 255-color)


# HELPER FUNCTIONS

def correlate(image, kernel, boundary_behavior):
    """
    Compute the result of correlating the given image with the given kernel.
    `boundary_behavior` will one of the strings "zero", "extend", or "wrap",
    and this function will treat out-of-bounds pixels as having the value zero,
    the value of the nearest edge, or the value wrapped around the other edge
    of the image, respectively.

    if boundary_behavior is not one of "zero", "extend", or "wrap", return
    None.

    Otherwise, the output of this function should have the same form as a 6.101
    image (a dictionary with "height", "width", and "pixels" keys), but its
    pixel values do not necessarily need to be in the range [0,255], nor do
    they need to be integers (they should not be clipped or rounded at all).

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.

    DESCRIBE YOUR KERNEL REPRESENTATION HERE

    I will represent kernels as squares with rows and columns where the leftmost top
    cell is indexed [0, 0]. By the way, I assume that the input kernel is a list of
    values [0 - 255]. So, I can easily computer the width and height by finding the
    square root of the total number of items in the list, given that it's always a
    square.
    """
    if boundary_behavior not in ["zero", "extend", "wrap"]:
        return None

    # Since kernel is always a square, we can use the math.sqrt() to find its width
    width = int(math.sqrt(len(kernel)))
    result = {
        "height": image["height"],
        "width": image["width"],
        "pixels": image["pixels"][:],
    }

    for row in range(image["height"]):
        for col in range(image["width"]):

            # Multiply kernel to this cell and its neighbouring cells
            temp_prod = 0 # Temporary product
            for k_row in range(int(-(width-1)/2), int((width-1)/2)+1):
                for k_col in range(int(-(width-1)/2), int((width-1)/2)+1):
                    kernel_pix = get_kernel_pixel(kernel, k_row + int((width-1)/2), k_col + int((width-1)/2))
                    img_pix = get_pixel(image, k_row+row, k_col+col, boundary_behavior)
                    temp_prod += (kernel_pix * img_pix)

            set_pixel(result, row, col, temp_prod)
    return result


def round_and_clip_image(image):
    """
    Given a dictionary, ensure that the values in the "pixels" list are all
    integers in the range [0, 255].

    All values should be converted to integers using Python's `round` function.

    Any locations with values higher than 255 in the input should have value
    255 in the output; and any locations with values lower than 0 in the input
    should have value 0 in the output.
    """
    new_image = image["pixels"][:]
    img_pix=image["pixels"]
    for i in range(len(img_pix)):
        if img_pix[i] < 0:
            new_image[i] = 0
        elif img_pix[i] > 255:
            new_image[i] = 255
        elif not isinstance(img_pix[i], int):
            new_image[i] = round(image["pixels"][i])

    return {"height":image["height"], "width":image["width"], "pixels":new_image}


# FILTERS

def blurred(image, kernel_size):
    """
    Return a new image representing the result of applying a box blur (with the
    given kernel size) to the given input image.

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.
    """
    # first, create a representation for the appropriate n-by-n kernel (you may
    # wish to define another helper function for this)

    # then compute the correlation of the input image with that kernel

    # and, finally, make sure that the output is a valid image (using the
    # helper function from above) before returning it.

    kernel = get_blur_kernel(kernel_size)
    correlated_img = correlate(image, kernel, "extend")
    return round_and_clip_image(correlated_img)

def sharpened(image, n):
    """
    Returns an image resulting from substracting and "unsharp" (blurred) version
    of the image from the scaled original image.

    If we have an image (I) and a blurred version of that image (B), then the value
    of the sharpened image (S) at a particular location is:
    S = 2*I - B
    """
    image_pix = image["pixels"]
    kernel = get_blur_kernel(n)
    blurred_img = correlate(image, kernel, "extend")

    # Computer S = 2*I - B
    sharpened_pix = [(2*image_pix[i] - blurred_img["pixels"][i]) for i in range(len(image_pix))]
    sharpened_img = {"height":image["height"], "width":image["width"], "pixels":sharpened_pix}
    return round_and_clip_image(sharpened_img)

def edges(image):
    """
    This filter uses two kernels: K1 and K2.

    After correlating the input image with these two kernels (using "extend" behavior),
    O1 and O2, each pixel of the output is the square root of the sum of the squares
    of corresponding pixels in O1 and O2.

    O = round(sqrt(O1**2 + O2**2))
    """
    kernel_1 = [
        -1, -2, -1,
        0, 0, 0,
        1, 2, 1,
    ]
    kernel_2 = [
        -1, 0, 1,
        -2, 0, 2,
        -1, 0, 1,
    ]
    correlation_1 = correlate(image, kernel_1, "extend")
    correlation_2 = correlate(image, kernel_2, "extend")

    # Computer O from O1 and O2
    edge_pix =[round(math.sqrt(c1**2 + c2**2)) for c1, c2 in zip(correlation_1["pixels"], correlation_2["pixels"])]
    edge_img = {"height": image["height"], "width": image["width"], "pixels": edge_pix}
    return round_and_clip_image(edge_img)

# HELPER FUNCTIONS FOR LOADING AND SAVING IMAGES

def load_greyscale_image(filename):
    """
    Loads an image from the given file and returns a dictionary
    representing that image.  This also performs conversion to greyscale.

    Invoked as, for example:
       i = load_greyscale_image("test_images/cat.png")
    """
    with open(filename, "rb") as img_handle:
        img = Image.open(img_handle)
        img_data = img.getdata()
        if img.mode.startswith("RGB"):
            pixels = [round(.299 * p[0] + .587 * p[1] + .114 * p[2])
                      for p in img_data]
        elif img.mode == "LA":
            pixels = [p[0] for p in img_data]
        elif img.mode == "L":
            pixels = list(img_data)
        else:
            raise ValueError(f"Unsupported image mode: {img.mode}")
        width, height = img.size
        return {"height": height, "width": width, "pixels": pixels}


def save_greyscale_image(image, filename, mode="PNG"):
    """
    Saves the given image to disk or to a file-like object.  If filename is
    given as a string, the file type will be inferred from the given name.  If
    filename is given as a file-like object, the file type will be determined
    by the "mode" parameter.
    """
    out = Image.new(mode="L", size=(image["width"], image["height"]))
    out.putdata(image["pixels"])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()


if __name__ == "__main__":
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place for
    # generating images, etc.
    pass

    # bluegill = load_greyscale_image("test_images/bluegill.png")
    # bluegill_inverted = inverted(bluegill)
    # save_greyscale_image(bluegill_inverted, "test_images/bluegill_inverted.png")

    # image={
    #     "height": 2,
    #     "width": 2,
    #     "pixels": [-3.4, 23, 267, 23.5]
    # }
    # print(image)
    # round_and_clip_image(image)
    # print(image)

    # pigbird = load_greyscale_image("test_images/pigbird.png")
    # kernel = [
    #     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    #     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    #     1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    #     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    #     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    #     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    #     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    #     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    #     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    #     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    #     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    #     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    #     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    # ]

    # correlated_pigbird = correlate(pigbird, kernel, "wrap")
    # rounded_pigbird = round_and_clip_image(correlated_pigbird)
    # save_greyscale_image(rounded_pigbird, "test_images/correlated_img.png")

    # cat = load_greyscale_image("test_images/cat.png")
    # blurred_cat = blurred(cat, 13)
    # save_greyscale_image(blurred_cat, "test_images/blurred_cat.png")

    # python = load_greyscale_image("test_images/python.png")
    # sharpened_python = sharpened(python, 11)
    # save_greyscale_image(sharpened_python, "test_images/sharpened_python.png")

    # construct = load_greyscale_image("test_images/construct.png")
    # edges_construct = edges(construct)
    # save_greyscale_image(edges_construct, "test_images/edges_construct.png")
