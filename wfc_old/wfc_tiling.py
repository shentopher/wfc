"""
Tiling takes an input image and breaks it up into tiles of size N x N 
Tile size is most likely to be 1 for pixel images. Bigger for larger files.
"""

import numpy as np
from numpy.typing import NDArray
from wfc_helper import hash_ndarray
from typing import Dict, Tuple

"""
@params: 
img (NDArray image), 
tilesize (N for N x N tile)
@outputs: 
tile_dictionary (dictionary with a hash as a key and tile NDArray as value)
hash_grid (grid of original image with tiles as values)
hash_list 1D representatino of hash_grid
tile_set (a set of tuples, which contains the tile ID and their frequency)
"""
def catalog_tiles(img: NDArray[np.integer], tile_size: int):
    num_channels = img.shape[2] # number of channels in image, given rgb it should be 3
    tiles = image_to_tiles(img, tile_size)

    tile_list: NDArray[np.integer] = tiles.reshape((tiles.shape[0] * tiles.shape[1], tile_size, tile_size, num_channels))

    hash_grid: NDArray[np.int64] = hash_ndarray(tiles, 2)
    hash_list: NDArray[np.int64] = hash_grid.reshape((tiles.shape[0] * tiles.shape[1]))
    tile_set: Tuple[NDArray[np.int64], NDArray[np.int64]] = np.unique(hash_grid, return_counts=True)

    tile_dictionary: Dict[int, NDArray[np.integer]] = dict()
    for i, j in enumerate(hash_list):
        # hash as key, ndarray as value
        tile_dictionary[j] = tile_list[i]
    
    return tile_dictionary, hash_grid, hash_list, tile_set



"""
Iterates through an input image and generates N x N tiles to feed into the WFC algorithm.
@params: 
img (NDArray image, 3 dimensional including width, height, and RGB channels)
tilesize (N for N x N tile)
@outputs::
tiles (an NDArray of tiles)
"""
def image_to_tiles(img: NDArray[np.integer], tile_size: int) -> NDArray[np.integer]:
    padding_argument = [(0, 0), (0, 0), (0, 0)]
    for input_dim in [0, 1]:
        padding_argument[input_dim] = (
            0,
            (tile_size - img.shape[input_dim]) % tile_size,
        )
    img = np.pad(img, padding_argument, mode="constant")
    tiles = img.reshape(
        (
            img.shape[0] // tile_size,
            tile_size,
            img.shape[1] // tile_size,
            tile_size,
            img.shape[2],
        )
    ).swapaxes(1, 2)
    return tiles

