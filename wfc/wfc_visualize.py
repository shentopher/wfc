import numpy as np
import imageio 

def render_to_output(hash_grid, hash_to_pattern, output_filename, pattern_size):
    tile_dtype = next(iter(hash_to_pattern.values())).dtype

    new_img = np.zeros(
        ( 
            hash_grid.shape[0] * pattern_size,
            hash_grid.shape[1] * pattern_size,
            3
        ),
        dtype=tile_dtype
    )

    print(new_img.shape)

    for i in range(hash_grid.shape[0]):
        for j in range(hash_grid.shape[1]):
            this_hash = hash_grid[i,j]
            tile = hash_to_pattern[this_hash]
            
            for u in range(pattern_size):
                for v in range(pattern_size):
                    pixel = tile[u, v]
                    
                    new_img[
                        (i * pattern_size) + u, (j * pattern_size) + v
                    ] = np.resize(
                        pixel,
                        new_img[
                            (i * pattern_size) + u, (j * pattern_size) + v
                        ].shape,
                    )
    
    imageio.imwrite(output_filename, new_img.astype(np.uint8))

def hashes_grid_to_tiles(solutions_as_hashes, hash_to_patterns):

    def pattern_to_tile(pattern):
        print(len(pattern))
        return hash_to_patterns[pattern][0]
    
    return np.vectorize(pattern_to_tile)(solutions_as_hashes)
