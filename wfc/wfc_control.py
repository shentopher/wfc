"""
The control file for wfc. Where the end-user interacts with the algorithm and runs it.
"""
# libraries
from typing import Tuple
import datetime
import imageio.v2
import numpy as np

# methods
from wfc_pattern import image_to_patterns
from wfc_hashing import hash_pattern_list
from wfc_adjacency import get_adjacencies, make_adj
from wfc_solver import make_wave, run
from wfc_visualize import hashes_grid_to_tiles, render_to_output

def runner(
    img_name: str,
    pattern_size: int=2,
    output_size: Tuple[int, int]=(20, 20),
    floor:bool = True,
    attempt_limit:int = 10
):
    # define constants
    input_folder = "./images/"
    output_folder = "./output/"
    timecode = datetime.datetime.now().isoformat().replace(":", ".")

    # load image
    image = imageio.imread(input_folder + img_name + ".png")[:, :, :3]
    if image is None:
        raise TypeError("Invalid Image Input")
    print("Image Shape: " + str(image.shape))

    # convert image to pattern information
    pattern_list, pattern_catalog, new_image, xtiles, ytiles = image_to_patterns(image, pattern_size)
    print("Number of Nonunique Patterns: " + str(len(pattern_list)))

    # get hash information
    hash_to_patterns, unique_patterns = hash_pattern_list(pattern_list)

    # get adjacency information
    adjacency_information = get_adjacencies(pattern_catalog, xtiles, ytiles)
    print("Number of Unique Patterns: " + str(len(adjacency_information)))

    # make wave
    wave = make_wave(unique_patterns, output_size)
    print("Wave Shape: " + str(wave.shape))

    # solve WFC
    time_start = None
    time_end = None
    attempt = 0

    while attempt < attempt_limit:
        attempt += 1
        wave = wave.copy()
        print("Starting Attempt " + str(attempt))
        
        collapsed_wave = run(wave, floor, adjacency_information)

    index_to_hash = sorted(list(adjacency_information.keys()))
    solution_as_hash = np.vectorize(lambda x: index_to_hash[x])(collapsed_wave)
    
    render_to_output(solution_as_hash, hash_to_patterns, output_folder+img_name+"_"+timecode+".png", pattern_size)

if __name__ == '__main__':
    image_name = "Skyline2"
    runner(image_name, attempt_limit=1)
