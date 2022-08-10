from numpy.typing import NDArray
import numpy as np

"""
Process image information to create a pattern catalog
@params:
image: NDArray[np.int64] tile informatoin
pattern_size: 
@output:
pattern_list
pattern_catalog: a tuple (x, y) of the position as key an an NDArray as output, where NDArray is of dimension (pattern_size, pattern_size, 3)
"""
def image_to_patterns(img: NDArray[np.integer], pattern_size: int):
    padding_argument = [(0, 0), (0, 0), (0, 0)]
    for input_dim in [0, 1]:
        padding_argument[input_dim] = (
            0,
            (pattern_size - img.shape[input_dim]) % pattern_size,
        )
    img = np.pad(img, padding_argument, mode="constant")

    xdim, ydim, _ = img.shape
    xtiles = int(xdim / pattern_size)
    ytiles = int(ydim / pattern_size)

    pattern_list = list()
    pattern_catalog = dict()

    for x in range(xtiles):
        for y in range(ytiles):
            lowx, lowy = 2 * x, 2 * y
            upx, upy = lowx + 2, lowy + 2
            pattern = img[lowx:upx, lowy:upy, :3]

            pattern_list.append(pattern)
            
            indices = (x, y)
            pattern_catalog[indices] = pattern

    return pattern_list, pattern_catalog, img, xtiles, ytiles


def pattern_catalog_to_unique_patterns(pattern_catalog):
    unique_patterns = dict()

    for key, value in pattern_catalog.items():
        pass
    pass