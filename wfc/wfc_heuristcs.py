"""
HEURISTICS
"""
from numpy.typing import NDArray
import numpy as np
from typing import Any, Callable, Tuple

# pattern heuristics
def makeWeightedPatternHeuristic(weights: NDArray[np.floating[Any]]):
    num_patterns = len(weights)

    def weightedPatternHeuristic(wave: NDArray[np.bool_], _: NDArray[np.bool_]) -> int:
        weighted_wave = weights * wave
        weighted_wave = weighted_wave / weighted_wave.sum()
        result = np.random.choice(num_patterns, p=weighted_wave)

        return result

    return weightedPatternHeuristic

# location heuristics
def makeEntropyLocationHeuristic(preferences: NDArray[np.floating[Any]]) -> Callable[[NDArray[np.bool_]], Tuple[int, int]]:
    def entropyLocationHeuristic(wave: NDArray[np.bool_]) -> Tuple[int, int]:
        unresolved_cell_mask = np.count_nonzero(wave, axis=0) > 1
        cell_weights = np.where(
            unresolved_cell_mask,
            preferences + np.count_nonzero(wave, axis=0),
            np.inf,
        )
        row, col = np.unravel_index(np.argmin(cell_weights), cell_weights.shape)

        return row.item(), col.item()

    return entropyLocationHeuristic