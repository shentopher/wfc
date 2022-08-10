import numpy as np
from numpy.typing import NDArray
from typing import Any

"""
Taken from Karth's wfc_utilies 
@params: 
tiles: NDArray
rank: the index of the hash (2 given that we are working with 2d images)
@outputs: 
hashed_tiles: hashes in the dimensions of tiles up to index=rank
"""
def hash_ndarray(a: NDArray[np.integer], rank:int, seed: Any=0):
    state = np.random.RandomState(seed)
    assert rank < len(a.shape)
    u: NDArray[np.integer] = a.reshape((np.prod(a.shape[:rank], dtype=np.int64), -1))
    v = state.randint(1 - (1 << 63), 1 << 63, np.prod(a.shape[rank:]), dtype=np.int64)
    return np.asarray(np.inner(u, v).reshape(a.shape[:rank]), dtype=np.int64)

