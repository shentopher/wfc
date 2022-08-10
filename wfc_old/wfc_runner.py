from typing import Type
import imageio
import numpy as np
from typing import Dict, Tuple, List, Set
import datetime
from numpy.typing import NDArray
import time

# local imports
from wfc_tiling import catalog_tiles
from wfc_pattern import make_pattern_catalog, pattern_grid_to_tiles
from wfc_adjacency import extract_adjacency
from wfc_solver import makeWave, makeAdj, run, StopEarly, TimedOut, Contradiction
from wfc_heuristics import makeWeightedPatternHeuristic, makeEntropyLocationHeuristic
from wfc_output import render_tiles_to_output

def runner_main(filename:str, 
                tile_size:int = 1,
                pattern_size:int = 2,
                output_size=[48,48],
                loc_heuristic="entropy",
                choice_heuristic="weighted",
                attempt_limit=10,
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

    if choice_heuristic == "weighted":
        pattern_heuristic = makeWeightedPatternHeuristic(encoded_weights)

    if loc_heuristic == "entropy":
        location_heuristic = makeEntropyLocationHeuristic(choice_random_weighting)
    
    # Constraints 
    active_global_constraints = lambda wave: True
    combined_constraints = [active_global_constraints]
    def combinedConstraints(wave: NDArray[np.bool_]) -> bool:
        # basically returns True in our implementatoin
        # currently just sets a framework for additional global constraints
        return all(fn(wave) for fn in combined_constraints)
    
    # Solve WFC
    time_start = None
    time_end = None

    attempts = 0

    while attempts < attempt_limit:
        attempts += 1
        print("Starting Attempt " + str(attempts) + "...")
        time_start = time.perf_counter()
        
        try:
            solution = run(
                wave.copy(),
                adjacency_matrix,
                location_heuristic,
                pattern_heuristic,
                periodic=True,
                backtracking=False,
                onChoice=None,
                onBacktrack=None,
                onObserve=None,
                onPropagate=None,
                onFinal=None,
                checkFeasible=combinedConstraints
            )
            solution_as_ids = np.vectorize(lambda x: decode_patterns[x])(solution)
            solution_tile_grid = pattern_grid_to_tiles(solution_as_ids, pattern_catalog)

            render_tiles_to_output(
                solution_tile_grid,
                tile_dictionary,
                (tile_size, tile_size),
                output_folder+filename+"_"+timecode+".png"
            )

            time_end = time.perf_counter()
            print("Attempt " + str(attempts) + " Successful: " + str(timecode))

        except StopEarly:
            print("Stopping Early")
            raise
        except TimedOut:
            print("Timed Out")
        except Contradiction as exc:
            print("Contradiction")

        finally:
            out_stats = {
                "attempts": attempts,
                "time_start": time_start,
                "time_end": time_end,
                "pattern_count": number_of_patterns
            }

            print(out_stats)

            return out_stats


def load_image(filename, input_folder):
    image = imageio.v2.imread(input_folder + filename + ".png")[:, :, :3] #keep only size 3 on z-axis
    if image is None:
        raise TypeError("Invalid image.")
    return image


# for testing purposes
if __name__ == '__main__':
    image_name = "Skyline2"
    runner_main(image_name)