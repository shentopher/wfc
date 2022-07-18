from typing import Type
import imageio
import numpy as np

# local imports
from wfc_tiling import catalog_tiles
from wfc_pattern import make_pattern_catalog
from wfc_adjacency import extract_adjacency


def runner_main(filename:str, 
                tile_size:int = 1,
                pattern_size:int = 2,
                output_size=[48,48]):

    img = load_image(filename)
    direction_offsets = list(enumerate([(0, -1), (1, 0), (0, 1), (-1, 0)]))
    
    # retrieve tile and pattern information
    tile_dictionary, hash_grid, hash_list, tile_set = catalog_tiles(img, tile_size)
    (pattern_catalog, pattern_weights, pattern_list, pattern_grid) = make_pattern_catalog(hash_grid, tile_size, periodic_input=True)

    # extract adjacency information
    adjacency_relations = extract_adjacency(
        pattern_grid=pattern_grid,
        pattern_dictionary=pattern_catalog,
        direction_offsets=direction_offsets,
        pattern_size=(pattern_size, pattern_size)
    )


def load_image(filename):
    image = imageio.v2.imread("images/" + filename + ".png")[:, :, :3] #keep only size 3 on z-axis
    if image is None:
        raise TypeError("Invalid image.")
    return image


# for testing purposes
if __name__ == '__main__':
    # flowers is 23 by 15 by 3
    image_name = "Town"
    runner_main(image_name)