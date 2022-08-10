# Write results to a new image file
import numpy as np
import imageio

def render_tiles_to_output(tile_grid, tile_catalog, tile_size, output_filename):
    img = tile_grid_to_image(tile_grid.T, tile_catalog, tile_size)
    imageio.imwrite(output_filename, img.astype(np.uint8))

def tile_grid_to_image(tile_grid, tile_catalog, tile_size, visualize=False, partial=False, color_channels=3):
    tile_dtype = next(iter(tile_catalog.values())).dtype
    new_img = np.zeros(
        (
            tile_grid.shape[0] * tile_size[0],
            tile_grid.shape[1] * tile_size[1],
            color_channels,
        ),
        dtype=tile_dtype
    )

    for i in range(tile_grid.shape[0]):
        for j in range(tile_grid.shape[1]):
            tile = tile_grid[i,j]
            for u in range(tile_size[0]):
                for v in range(tile_size[1]):
                    pixel = tile_catalog[tile][u, v]
                    new_img[
                            (i * tile_size[0]) + u, (j * tile_size[1]) + v
                        ] = np.resize(
                            pixel,
                            new_img[
                                (i * tile_size[0]) + u, (j * tile_size[1]) + v
                            ].shape,
                        )
    return new_img
