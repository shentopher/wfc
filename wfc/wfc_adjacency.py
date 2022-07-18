"""
Take pattern information and identify adjacencies
"""

from typing import Dict, List, Tuple
from numpy.typing import NDArray
import numpy as np

"""
@params:
pattern_grid
pattern_dictionary
direction offsets
pattern_size
@outputs
legal -> List[Tuple[Tuple[int, int], int, int]]: direction tuple, pattern1 hash, pattern2 hash
"""
def extract_adjacency(pattern_grid: NDArray[np.int64], pattern_dictionary: Dict[int, NDArray[np.int64]], direction_offsets: List[Tuple[int, Tuple[int, int]]],
    pattern_size: Tuple[int, int] = (2, 2),):

    legal = [] 
    patterns = list(pattern_dictionary.keys())

    for pattern1 in patterns:
        for pattern2 in patterns:
            for _, direction in direction_offsets:
                if matching_over_intersection(direction, pattern1, pattern2, pattern_dictionary, pattern_size):
                    legal.append((direction, pattern1, pattern2))

    return legal

"""
Determins if two patterns form a valid intersection
@params
adjacency_directions: a tuple of integers specifiying pattern matching directions
pattern1
pattern2
pattern catalog
pattern size
@outputs
res: a boolean for whether a valid intersection exists
"""
def matching_over_intersection(adjacency_direction, pattern1, pattern2, pattern_catalog, pattern_size):
    dimensions = (1, 0)

    pad = np.pad(pattern_catalog[pattern2], max(pattern_size), mode="constant", constant_values=-1)
    shifted = np.roll(a=pad, shift=adjacency_direction, axis=dimensions)

    # ex. shifted[2:4] gives a slice
    compare = shifted[
        pattern_size[0] : pattern_size[0] + pattern_size[0],
        pattern_size[1] : pattern_size[1] + pattern_size[1]
    ]

    left = max(0, 0 + adjacency_direction[0])
    right = min(pattern_size[0], pattern_size[0] + adjacency_direction[0])

    top = max(0, 0 + adjacency_direction[1])
    bottom = min(pattern_size[1], pattern_size[1] + adjacency_direction[1])

    a = pattern_catalog[pattern1][top:bottom, left:right]
    b = compare[top:bottom, left:right]

    res = np.array_equal(a, b)

    return res


