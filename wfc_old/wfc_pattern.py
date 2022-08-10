"""
Take N x N tiles that were created in wfc_tiling and encodes pattern information
Typical pattern size is 2 or 3 (default 2)
"""
from typing import Any, Dict, Mapping, Optional, Tuple
from wfc_helper import hash_ndarray
from collections import Counter
import numpy as np
from numpy.typing import NDArray

"""
Creates a pattern catalog based off of tile information
@params:
tile_grid: NDArray[np.int64] of tile information
pattern_width: int
periodic_input: whether input wraps at edges
@output:
a tuple containing
    pattern catalog (key: hash, value: constituent tile)
    pattern_frequency: Counter
    pattern_content_list: a list of pattern weights
    patch_codes
"""
def make_pattern_catalog(tile_grid: NDArray[np.int64], pattern_width:int, periodic_input=True
    ) -> Tuple[Dict[int, NDArray[np.int64]], Counter, NDArray[np.int64], NDArray[np.int64]]:
    
    patterns_grid, pattern_contents_list, patch_hashes = unique_patterns(
        tile_grid, pattern_width, periodic_input
    )

    pattern_contents_dict = dict()

    for pattern_index in range(pattern_contents_list.shape[0]):
        pattern_hash = hash_ndarray(pattern_contents_list[pattern_index], 0)
        pattern_contents_dict.update(
            {pattern_hash.item() : pattern_contents_list[pattern_index]}
        )

    pattern_frequency = Counter(hash_ndarray(pattern_contents_list, 1))

    pattern_contents_list = hash_ndarray(pattern_contents_list, 1)

    return (pattern_contents_dict, pattern_frequency, pattern_contents_list, patch_hashes)



"""
References Karth's Implementation

Finds all unique patterns from a grid of tiles
@params:
grid: grid of tiles
stride: int
periodic_input: whether input wraps at edges
"""
def unique_patterns(grid: NDArray[np.int64], stride: int, periodic_input: bool) -> Tuple[NDArray[np.int64], NDArray[np.int64], NDArray[np.int64]]:
    assert stride >= 1
    if periodic_input:
        grid = np.pad(
            grid,
            ((0, stride - 1), (0, stride - 1), *(((0, 0),) * (len(grid.shape) - 2))),
            mode="wrap",
        )
    else:
        # TODO: implement non-wrapped image handling
        grid = np.pad(
            grid,
            ((0, stride - 1), (0, stride - 1), *(((0, 0),) * (len(grid.shape) - 2))),
            mode="wrap",
        )
    
    strides = (grid.shape[0] - stride + 1, grid.shape[1] - stride + 1, stride, stride, *grid.shape[2:])

    patches: NDArray(np.int64) = np.lib.stride_tricks.as_strided(
        grid,
        strides,
        grid.strides[:2] + grid.strides[:2] + grid.strides[2:],
        writeable=False
    )

    patch_hashes = hash_ndarray(patches, 2)
    unique_hashes, unique_indices = np.unique(patch_hashes, return_index=True)
    locs = np.unravel_index(unique_indices, patch_hashes.shape)

    up: NDArray[np.int64] = patches[locs[0], locs[1]]
    ids: NDArray[np.int64] = np.vectorize({code: ind for ind, code in enumerate(unique_hashes)}.get)(patch_hashes)

    return ids, up, patch_hashes


def pattern_grid_to_tiles(pattern_grid, pattern_catalog) -> NDArray[np.int64]:
    anchor_x, anchor_y = 0, 0

    def pattern_to_tile(pattern):
        return pattern_catalog[pattern][anchor_x][anchor_y]

    return np.vectorize(pattern_to_tile)(pattern_grid)