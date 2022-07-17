from typing import Type
import imageio
import numpy as np

from wfc_tiling import catalog_tiles
from wfc_tiling import image_to_tiles


def runner_main(filename):
    pass


def load_image(filename):
    image = imageio.v2.imread("images/" + filename + ".png")[:, :, :3] #keep only size 3 on z-axis
    if image is None:
        raise TypeError("Invalid image.")
    return image


# for testing purposes
if __name__ == '__main__':
    # flowers is 23 by 15 by 3
    image = load_image("Flowers")
    image_to_tiles(image, 2)
