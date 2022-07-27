from __future__ import annotations
from turtle import back

from numpy.typing import NDArray
import numpy as np
from typing import *
from scipy import sparse

def run(
    wave,
    adj,
    locationHeuristic,
    patternHeuristic,
    periodic=False,
    backtracking=False,
    onBacktrack=None,
    onChoice=None,
    onObserve=None,
    onPropagate=None,
    checkFeasible=None,
    onFinal=None,
    depth=0,
    depth_limit=0
) -> NDArray[np.int64]:
    solver = Solver(
        wave=wave,
        adj=adj,
        periodic=periodic,
        backtracking=backtracking,
        on_backtrack=onBacktrack,
        on_choice=onChoice,
        on_observe=onObserve,
        on_propogate=onPropagate,
        check_feasible=checkFeasible
    )
    while not solver.solve_next(locationHeuristic, patternHeuristic):
        pass
    if onFinal:
        onFinal(solver.wave)
    return np.argmax(solver.wave, axis=0)

class Solver():
    # main solving class
    def __init__(
        self,
        *,
        wave: NDArray[np.bool_],
        adj: Mapping[Tuple[int, int], NDArray[np.bool_]],
        periodic: bool = False,
        backtracking: bool = False,
        on_backtrack: Optional[Callable[[], None]] = None,
        on_choice: Optional[Callable[[int, int, int], None]] = None,
        on_observe: Optional[Callable[[NDArray[np.bool_]], None]] = None,
        on_propogate: Optional[Callable[[NDArray[np.bool_]], None]] = None,
        check_feasible: Optional[Callable[[NDArray[np.bool_]], bool]] = None,
    ) -> None:
        self.wave =wave
        self.adj = adj
        self.periodic = periodic
        self.backtracking = backtracking
        self.on_backtrack = on_backtrack
        self.on_choice = on_choice
        self.on_observe = on_observe
        self.on_propogate = on_propogate
        self.check_feasible = check_feasible
        self.history: List[NDArray[np.bool_]] = []

    def solve(self, location_heuristic, pattern_heuristic) -> NDArray[np.int64]:
        while not self.solve_next(location_heuristic, pattern_heuristic):
            pass
        return np.argmax(self.wave, axis=0)

    def is_solved(self) -> bool:
        # returns true if wave has been solved
        return self.wave.sum() == self.wave.shape[1] * self.wave.shape[2] and (self.wave.sum(axis=0) == 1).all()

    def solve_next(self, location_heuristic, pattern_heuristic) -> bool:
        # returns true if no more steps remain
        if self.is_solved:
            return True
        if self.check_feasible and not self.check_feasible(self.wave):
            raise Contradiction("Not feasible")
        if self.backtracking:
            self.history.append(self.wave.copy())

        propagate(self.wave, self.adj, self.periodic, self.on_propogate)

        try:
            pattern, i, j = observe(self.wave, location_heuristic, pattern_heuristic)
        except Contradiction:
            if not self.backtracking:
                raise
            if not self.history:
                raise Contradiction("Every permutation has been attempted.")
            if self.on_backtrack:
                self.on_backtrack
            # remove latest step
            self.wave = self.history.pop()
            self.wave[pattern, i, j] = False
            return False



# auxiliary functions for Solver Class
def propagate(wave, adj, periodic=False, onPropagate=None) -> None:
    # completely propogate result of collapse to the rest of the wave
    last_count = wave.sum()

    while True:
        supports = {}
        if periodic:
            padded = np.pad(wave, ((0, 0), (1, 1), (1, 1)), mode="wrap")
        else:
            padded = np.pad(wave, ((0, 0), (1, 1), (1, 1)), mode="constant", constant_values=True)

        # adj is a list of adjacencies. For each adjacency, check which is still valid
        for d in adj:
            dx, dy = d
            shifted = padded[
                :, 
                1 + dx : 1 + wave.shape[1] + dx, 
                1 + dy : 1 + wave.shape[2] + dy
            ]
        
        supports[d] = (adj[d] @ shifted.reshape(shifted.shape[0], -1)).reshape(shifted.shape) > 0

        for d in adj:
            wave *= supports[d]
        
        if wave.sum() == last_count:
            break
        last_count = wave.sum()

    if onPropagate:
        onPropagate(wave)
    
    if (wave.sum(axis=0) == 0).any():
        raise Contradiction("Wave cannot be solved")


def observe(wave, locationHeuristic, patternHeuristic) -> Tuple[int, int, int]:
    # returns the next best element in the wave to collapse
    i, j = locationHeuristic(wave)
    pattern = patternHeuristic(wave[:, i, j], wave)
    return pattern, i, j

# initialization methods
def makeWave(number_of_patterns: int, width: int, height: int, ground=None):
    wave = np.ones((number_of_patterns, width, height), dtype=np.bool_)
    return wave

def makeAdj(adjLists: Mapping[Tuple[int, int], Collection[Iterable[int]]]):
    adjMatrices = {}
    num_patterns = len(list(adjLists.values())[0])

    for d in adjLists:
        mat = np.zeros((num_patterns, num_patterns), dtype=bool)
        for i, js in enumerate(adjLists[d]):
            for j in js:
                mat[i, j] = 1
        adjMatrices[d] = sparse.csr_matrix(mat)
    return adjMatrices

# Exceptions
class Contradiction(Exception):
    """Solving could not proceed without backtracking/restarting."""
    pass


class TimedOut(Exception):
    """Solve timed out."""
    pass


class StopEarly(Exception):
    """Aborting solve early."""
    pass
