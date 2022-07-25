from typing import Type
import imageio
import numpy as np
from typing import Dict, Tuple, List, Set
import datetime
from numpy.typing import NDArray

# local imports
from wfc_tiling import catalog_tiles
from wfc_pattern import make_pattern_catalog
from wfc_adjacency import extract_adjacency
from wfc_solver import makeWave, makeAdj

def runner_main(filename:str, 
                tile_size:int = 1,
                pattern_size:int = 2,
                output_size=[48,48],
                loc_heuristics="entropy",
                choice_heuristic="weighted",
                attempt_limit=10
                ):
    
    # define constatns
    input_folder = "./images/"
    output_folder = "./output/"
    timecode = datetime.datetime.now().isoformat().replace(":", ".")

    # load image
    print("Loading Image...")
    img = load_image(filename, input_folder)
    direction_offsets = list(enumerate([(0, -1), (1, 0), (0, 1), (-1, 0)]))
    
    # retrieve tile and pattern information
    print("Extracting Tile and Patterns...")
    tile_dictionary, hash_grid, hash_list, tile_set = catalog_tiles(img, tile_size)
    (pattern_catalog, pattern_weights, pattern_list, pattern_grid) = make_pattern_catalog(hash_grid, tile_size, periodic_input=True)

    # extract adjacency information
    adjacency_relations = extract_adjacency(
        pattern_grid=pattern_grid,
        pattern_dictionary=pattern_catalog,
        direction_offsets=direction_offsets,
        pattern_size=(pattern_size, pattern_size)
    )

    # clean up pattern data
    number_of_patterns = len(pattern_weights)
    decode_patterns = dict(enumerate(pattern_list))
    encode_patterns = {x: i for i, x in enumerate(pattern_list)}
    _encode_directions = {j: i for i, j in direction_offsets}

    # clean up adjacency data
    adjacency_list: Dict[Tuple[int, int], List[Set[int]]] = {}
    for _, adjacency in direction_offsets:
        adjacency_list[adjacency] = [set() for _ in pattern_weights]
    for adjacency, pattern1, pattern2 in adjacency_relations:
        adjacency_list[adjacency][encode_patterns[pattern1]].add(encode_patterns[pattern2])

    # TODO: add ground functionality

    # prepare for WFC algo
    print("Making Wave...")
    wave = makeWave(number_of_patterns, output_size[0], output_size[1], ground=None)
    adjacency_matrix = makeAdj(adjacency_list)

    # Heuristics
    print("Encoding heuristics...")
    encoded_weights: NDArray[np.float64] = np.zeros((number_of_patterns), dtype=np.float64)
    for weight_id, weight_val in pattern_weights.items():
        encoded_weights[encode_patterns[weight_id]] = weight_val
    choice_random_weighting: NDArray[np.float64] = np.random.random_sample(wave.shape[1:]) * 0.1

    # Constraints 
    active_global_constraints = lambda wave: True
    combined_constraints = [active_global_constraints]
    def combinedConstraints(wave: NDArray[np.bool_]) -> bool:
        # basically returns True in our implementatoin
        # setting up a framework for additional global constraints though
        return all(fn(wave) for fn in combined_constraints)
    
    # Solve WFC
    start_solve_time = None
    end_solve_time = None

    attempt = 0

    while attempt < attempt_limit:
        attempt += 1
        print("Starting Attempt " + str(attempt) + "...")

        stats = {}
        
        try:
            pass

        finally:
            pass


def load_image(filename, input_folder):
    image = imageio.v2.imread(input_folder + filename + ".png")[:, :, :3] #keep only size 3 on z-axis
    if image is None:
        raise TypeError("Invalid image.")
    return image


# for testing purposes
if __name__ == '__main__':
    # flowers is 23 by 15 by 3
    image_name = "Town"
    runner_main(image_name)