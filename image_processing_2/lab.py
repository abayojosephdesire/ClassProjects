#!/usr/bin/env python3

"""
6.101 Lab 2:
Image Processing 2
"""

# NO ADDITIONAL IMPORTS!
# (except in the last part of the lab; see the lab writeup for details)
import math
from PIL import Image


# VARIOUS FILTERS

########## TAKEN FROM Lab 1 --- with minimal modifications
def get_pixel(image, row, col, boundary_behavior=None):
    """
    Returns the value [0-255] at (row, col)
    """

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


def set_pixel(image, row, col, color):
    """ Sets the value of the pixel at (row, col) position."""
    width = image["width"]
    image["pixels"][(row)*width + col] = color


def apply_per_pixel(image, func):
    """Applies function func on every pixel of the image."""
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

def get_kernel_pixel(kernel, row, col):
    """
    Returns the pixels at (row, col) in the kernel.
    """
    width = int(math.sqrt(len(kernel)))
    return kernel[(row*width) + col]

def get_blur_kernel(kernel_size):
    """
    Returns a kernel used for blurring images.
    """
    kernel_pix = 1/ (kernel_size**2)
    return [kernel_pix for _ in range(kernel_size**2)]


def inverted(image):
    """ Inverts the image in such a way that the black spot becomes bright and vice versa."""
    return apply_per_pixel(image, lambda color: 255-color)

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


########## END of functions copied from Lab 1



def get_one_d_pix(color_img, color):
    """Given a color image and an RGB type ("r for red", "g for green", and "b for blue"), return a grey image
    corresponding to that type. Please note that we return an image with pixels of 1-d not 3-d as in color image.
    """
    # Let i represent RGB: 0 == r(red), 1 == g(green), and 2 == b(blue)
    if color == "r": i = 0
    elif color == "g": i = 1
    else: i = 2
    img_pix = color_img["pixels"]
    return {
        "height":color_img["height"],
        "width":color_img["width"],
        "pixels":[img_pix[j][i] for j in range(len(img_pix))],
        }

def color_filter_from_greyscale_filter(filt):
    """
    Given a filter that takes a greyscale image as input and produces a
    greyscale image as output, returns a function that takes a color image as
    input and produces the filtered color image.
    """
    def color_filter(color_img):
        r_img = filt(get_one_d_pix(color_img, "r"))["pixels"]
        g_img = filt(get_one_d_pix(color_img, "g"))["pixels"]
        b_img = filt(get_one_d_pix(color_img, "b"))["pixels"]

        return {
            "height": color_img["height"],
            "width": color_img["width"],
            "pixels": [(r, g, b) for r, g, b in zip(r_img, g_img, b_img)]
        }

    return color_filter


def make_blur_filter(kernel_size):
    """
    Takes in kernel_size as an argument and returns a blurred filter function that only
    takes in an image as an argument. This can then be passed in functions like
    "color_filter_from_greyscale_filter"
    """
    kernel = get_blur_kernel(kernel_size)
    def blur_filter(image):
        correlated_img = correlate(image, kernel, "extend")
        return round_and_clip_image(correlated_img)

    return blur_filter


def make_sharpen_filter(kernel_size):
    """
    Takes in kernel_size as an argument and returns a sharpen filter function that only
    takes in an image as an argument. This can then be passed in functions like
    "color_filter_from_greyscale_filter"
    """
    def sharp_filter(image):
        image_pix = image["pixels"]
        kernel = get_blur_kernel(kernel_size)
        blurred_img = correlate(image, kernel, "extend")

        # Computer S = 2*I - B
        sharpened_pix = [(2*image_pix[i] - blurred_img["pixels"][i]) for i in range(len(image_pix))]
        sharpened_img = {"height":image["height"], "width":image["width"], "pixels":sharpened_pix}
        return round_and_clip_image(sharpened_img)

    return sharp_filter

def filter_cascade(filters):
    """
    Given a list of filters (implemented as functions on images), returns a new
    single filter such that applying that filter to an image produces the same
    output as applying each of the individual ones in turn.
    """
    def single_filter(image):
        for filter in filters:
            image = filter(image)
        return image

    return single_filter


# SEAM CARVING

# Main Seam Carving Implementation


def seam_carving(image, ncols):
    """
    Starting from the given image, use the seam carving technique to remove
    ncols (an integer) columns from the image. Returns a new image.
    """
    carved_img = {
        "height": image["height"],
        "width": image["width"],
        "pixels": [(r, g, b) for (r, g, b) in image["pixels"]]
    }

    # Go though all the transformations
    for n in range(ncols):
        grey_img = greyscale_image_from_color_image(carved_img)
        energy = compute_energy(grey_img)
        cumulative_map = cumulative_energy_map(energy)
        min_seam = minimum_energy_seam(cumulative_map)
        carved_img = image_without_seam(carved_img, min_seam)
        print("Finished:", n+1, "step(s).")

    return carved_img

# Optional Helper Functions for Seam Carving


def greyscale_image_from_color_image(image):
    """
    Given a color image, computes and returns a corresponding greyscale image.

    Returns a greyscale image (represented as a dictionary).
    """
    grey_img = {
        "height": image["height"],
        "width": image["width"],
        "pixels": [],
    }

    for (r, g, b) in image["pixels"]:
        grey_img["pixels"].append(round(r*0.299 + g*0.587 + b*0.114))

    return grey_img


def compute_energy(grey):
    """
    Given a greyscale image, computes a measure of "energy", in our case using
    the edges function from last week.

    Returns a greyscale image (represented as a dictionary).
    """
    return edges(grey)


def cumulative_energy_map(energy):
    """
    Given a measure of energy (e.g., the output of the compute_energy
    function), computes a "cumulative energy map" as described in the lab 2
    writeup.

    Returns a dictionary with 'height', 'width', and 'pixels' keys (but where
    the values in the 'pixels' array may not necessarily be in the range [0,
    255].
    """
    height = energy["height"]
    width = energy["width"]
    cumulative_map = {
        "height": height,
        "width": width,
        "pixels": energy["pixels"][:width]
    }
    for row in range(1, height):
        for col in range(width):

            current_pix = get_pixel(energy, row, col)
            adjacent_pix = [get_pixel(cumulative_map, row-1, col),]

            #Handle the limits of the image
            if col != 0: adjacent_pix.append(get_pixel(cumulative_map, row-1, col-1))
            if col != width-1: adjacent_pix.append(get_pixel(cumulative_map, row-1, col+1))

            cumulative_map["pixels"].append(current_pix + min(adjacent_pix))

    return cumulative_map


def minimum_energy_seam(cem):
    """
    Given a cumulative energy map, returns a list of the indices into the
    'pixels' list that correspond to pixels contained in the minimum-energy
    seam (computed as described in the lab 2 writeup).
    """
    width = cem["width"]
    height = cem["height"]
    bottom_row = cem["pixels"][(width*(height-1)):]
    bottom_seam_index = bottom_row.index(min(bottom_row)) # Represents the col number of a cell of interest

    seam_indices = [((height-1)*width + bottom_seam_index), ]

    for row in range(height-2, -1, -1):

        # Set them to -ve infinity as we're interested in max of this list
        adjacent_pix = [float('inf'), get_pixel(cem, row, bottom_seam_index), float('inf')]
        if bottom_seam_index != 0: adjacent_pix[0] = (get_pixel(cem, row, bottom_seam_index-1))
        if bottom_seam_index != width-1: adjacent_pix[2] = (get_pixel(cem, row, bottom_seam_index+1))

        min_adjacent_pix = adjacent_pix.index(min(adjacent_pix))
        if min_adjacent_pix == 0: bottom_seam_index -= 1
        elif min_adjacent_pix == 2: bottom_seam_index += 1

        seam_indices.append(row*width + bottom_seam_index)

    return seam_indices



def image_without_seam(image, seam):
    """
    Given a (color) image and a list of indices to be removed from the image,
    return a new image (without modifying the original) that contains all the
    pixels from the original image except those corresponding to the locations
    in the given list.
    """
    return {
        "height": image["height"],
        "width": image["width"]-1,
        "pixels": [pix for pos, pix in enumerate(image["pixels"]) if pos not in seam]
    }

def right_to_left(image, width, height):
    """ Return a horizontally flipped image"""
    img_pix = []
    for row in range(height): img_pix += reversed(image["pixels"][width*row:width*(row+1)])
    return {"width": width, "height": height, "pixels": img_pix}

def bottom_to_top(image, width, height):
    """ Return a vertically flipped image"""
    img_pix = []
    for row in range(height, -1, -1): img_pix += image["pixels"][width*row:width*(row+1)]
    return {"width": width, "height": height, "pixels": img_pix}

def custom_feature(image, mirror):
    """
    Takes in an image and mirror arguments and returns a rotated image.
    {
        lt doesn't change the image,
        lb returns an image flipped vertically only,
        rt returns an image flipped horizontally only,
        rb returns an image flipped both vertically and horizontally
    }
    """
    width = image["width"]
    height = image["height"]
    if mirror not in ["lt", "lb", "rt", "rb"]: return None
    if mirror == "lt": return image
    if mirror == "lb": return bottom_to_top(image, width, height)
    if mirror == "rt": return right_to_left(image, width, height)
    if mirror == "rb": return right_to_left(bottom_to_top(image, width, height), width, height)

# HELPER FUNCTIONS FOR LOADING AND SAVING COLOR IMAGES


def load_color_image(filename):
    """
    Loads a color image from the given file and returns a dictionary
    representing that image.

    Invoked as, for example:
       i = load_color_image('test_images/cat.png')
    """
    with open(filename, "rb") as img_handle:
        img = Image.open(img_handle)
        img = img.convert("RGB")  # in case we were given a greyscale image
        img_data = img.getdata()
        pixels = list(img_data)
        width, height = img.size
        return {"height": height, "width": width, "pixels": pixels}



def save_color_image(image, filename, mode="PNG"):
    """
    Saves the given color image to disk or to a file-like object.  If filename
    is given as a string, the file type will be inferred from the given name.
    If filename is given as a file-like object, the file type will be
    determined by the 'mode' parameter.
    """
    out = Image.new(mode="RGB", size=(image["width"], image["height"]))
    out.putdata(image["pixels"])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()


def load_greyscale_image(filename):
    """
    Loads an image from the given file and returns an instance of this class
    representing that image.  This also performs conversion to greyscale.

    Invoked as, for example:
       i = load_greyscale_image('test_images/cat.png')
    """
    with open(filename, "rb") as img_handle:
        img = Image.open(img_handle)
        img_data = img.getdata()
        if img.mode.startswith("RGB"):
            pixels = [
                round(0.299 * p[0] + 0.587 * p[1] + 0.114 * p[2]) for p in img_data
            ]
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
    by the 'mode' parameter.
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

    # colorInverted = color_filter_from_greyscale_filter(inverted)
    # cat_inverted = colorInverted(load_color_image("test_images/cat.png"))
    # save_color_image(cat_inverted, "test_results/cat_inverted.png", mode="PNG")

    # blurredFilter = color_filter_from_greyscale_filter(make_blur_filter(9))
    # python_blurred = blurredFilter(load_color_image('test_images/python.png'))
    # save_color_image(python_blurred, "test_results/python_blurred.png", mode="PNG")

    # blurredFilter = color_filter_from_greyscale_filter(make_sharpen_filter(7))
    # sparrow_sharpened = blurredFilter(load_color_image('test_images/sparrowchick.png'))
    # save_color_image(sparrow_sharpened, "test_results/sparrowchick_sharpened.png", mode="PNG")

    # filter1 = color_filter_from_greyscale_filter(edges)
    # filter2 = color_filter_from_greyscale_filter(make_blur_filter(5))
    # filt = filter_cascade([filter1, filter1, filter2, filter1])
    # frog_filt = filt(load_color_image('test_images/frog.png'))
    # save_color_image(frog_filt, "test_results/frog_filt.png", mode="PNG")

    # carved_twocats = seam_carving(load_color_image("test_images/twocats.png"), 100)
    # save_color_image(carved_twocats, "test_results/carved_twocats.png", mode="PNG")

    # custom_img = custom_feature(load_color_image("test_images/bluegill.png"), "rb")
    # save_color_image(custom_img, "test_results/custom_img.png", mode="PNG")
