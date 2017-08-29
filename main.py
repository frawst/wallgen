"""
Background Image Generator
(C) Justyn Chaykowski 2017

Currently just a pixel generator, really.

Uses PIL to generate images.

Planned functionality:
    - Apply functional image generation on-top of an input image, such that
    the output image will represent the functions initial intention, but
    modified to enunciate the input image. i.e. it may use outlines or other
    image filter information to modify the base function's pixel map, making
    the input image darken/brighten pixels on the output, or perhaps other forms
    of manipulation.
    - This script is primarily intended as a testing zone for PIL image manips,
    and while it may create vibrant and interesting images eventually, it is not
    intended to be an extensible framework. Most functionality will remain in an
    internal-use-only format.
"""

from PIL import Image


def limit_rgb(in_v, limiter):
    """
    Takes a value and it's maximum potential and maps it to 0-255
    :param in_v: input value
    :param limiter: value's maximum potential
    :return: int
    """
    out_v = int((in_v/limiter) * 255)
    return out_v


def mast(width, height, o):
    """
    PIL Image generate and save

    Used to generate and save PIL images, should call pixel manipulating
    functions within this function to generate output image. All images
    passed to this function must be saved as a new variable before outputting.

    :param width: Image width
    :param height:  Image height
    :param o: Image output name
    :return: None
    """
    # Generate an image and post to o.jpg
    color_format = 'RGB'
    image_background = 'black'
    size = (width, height)
    outfile = '{}.jpg'.format(o)
    outformat = 'JPEG'

    img = Image.new(color_format, size, image_background)

    fc = from_center(img)

    fc.save(outfile, outformat)


def from_center(image):
    """
    Pixel Manipulator

    Manipulates pixels such that their color is based around the height middle
    is absolute green, higher pixels are more blue, and lower pixels are more
    red. Also creates a black bar on the left-most 240 pixels and creates a
    brightness gradient as the pixels move further away from the 240 pixel point

    :param image: PIL Image object
    :return: PIL Image object
    """
    pix = image.load()
    width = image.size[0]
    height = image.size[1]
    for i in range(width):
        for j in range(height):
            if i < 240:
                pix[i, j] = (0, 0, 0)
            else:
                if j > 540:
                    invert = limit_rgb(j - 540, 540)
                    pix[i, j] = (
                        limit_rgb(
                            (j - 540), 540
                        ),
                        (255 - invert),
                        0
                    )
                # elif j == 540:
                #     pix[i, j] = (0, 255, 0)
                else:
                    pix[i, j] = (
                        0,
                        limit_rgb(
                            j, 540
                        ),
                        limit_rgb(
                            540 - j, 540
                        )
                    )
                    # Darkening loop

    for i in range(width):
        a = 255 - limit_rgb(i - 240, 840)  # Brighter as move away
        for j in range(height):
            if i >= 240:
                pr = pix[i, j][0]
                pg = pix[i, j][1]
                pb = pix[i, j][2]
                if pr == 0:
                    bsum = pg + pb
                    pgperc = pg / bsum
                    pbperc = pb / bsum
                    pix[i, j] = (pr, pg - (int(a * pgperc)), pb - (int(a * pbperc)))
                elif pb == 0:
                    bsum = pr + pg
                    pgperc = pg / bsum
                    prperc = pr / bsum
                    pix[i, j] = (pr - (int(a * prperc)), pg - (int(a * pgperc)), pb)

    return image


# def gen_squares_and_random(image):
#     pixels = image.load()
#     height = image.size[0]
#     width = image.size[1]
#     rect1 = (image.size[0] * 0.8, image.size[1] * 0.8)
#     rect2 = (image.size[0] * 0.6, image.size[1] * 0.6)
#     rect3 = (image.size[0] * 0.4, image.size[1] * 0.4)
#     rect4 = (image.size[0] * 0.2, image.size[1] * 0.2)
#     for i in range(height):
#         for j in range(width):
#             pass
#     return image


def gen_on_size(image):
    """
    Pixel manipulator function

    Simple determines the pixel color based on the height and width of the image
    currently outputs purely black/white image. Originally a test function, but
    can be used as a start point for other functions.

    :param image: PIL Image Object
    :return: PIL Image Object
    """
    pix_array = image.load()
    height = image.size[0]
    width = image.size[1]
    for i in range(height):
        for j in range(width):
            pix_array[i, j] = (limit_rgb(i, height),
                               limit_rgb(j, width),
                               limit_rgb(i + j, height + width))

    return image

if __name__ == "__main__":
    mast(1920, 1080, 'bbar_progress_thirds_12')
