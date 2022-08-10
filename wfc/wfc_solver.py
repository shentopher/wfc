from random import randint
from typing import Tuple
import numpy as np
import random
import sys

from wfc_exceptions import Contradiction, TimedOut, StopEarly
from wfc_adjacency import make_adj

"""
@inputs: pattern_list, which is a list of all unique hashed patterns
         output_size, a tuple of the number of horiz and vertical elements in the output image
@outputs: wave, an 3DNDarray of Booleans with x dim, y dim, and number of patterns as z-axis. Default initializes to all True
"""
def make_wave(unique_patterns, output_size):
    xdim, ydim = output_size
    number_of_patterns = len(unique_patterns)
    wave = np.ones(shape=(xdim, ydim, number_of_patterns), dtype=bool)
    return wave

def run(wave, floor, adjacency_information):
    pattern_list = sorted(list(adjacency_information.keys()))

    solver = Solver(wave=wave, adjacency_information=adjacency_information, pattern_list=pattern_list, floor=floor)

    print("Init wave sum " + str(wave.sum()))

    print("Collapse First Elem")
    solver.collapse_first_elem()

    solve_counter = 0
    while not solver.solve_next():
        solve_counter += 1
        print("Current Solve Counter " + str(solve_counter))
        pass
    
    print("yes wave is solved")
    collapsed_wave = np.argmax(solver.wave, axis=2)
    print(collapsed_wave)

    return collapsed_wave


class Solver():
    def __init__(self, wave, adjacency_information, pattern_list, floor) -> None:
        self.adjacency_information = adjacency_information
        self.pattern_list = pattern_list
        self.floor = floor
        self.solved_count = 0
        self.wave = wave

    def solve_next(self):
        # check that we continue with solving
        if self.is_solved():
            print("Is Solved")
            return True
        if not self.check_solvable():
            print("Not Solvable")
            raise Contradiction("Not Solvable")
        
        # observe and then propogate next
        try:
            a0, a1 = observe_next(self.wave, self.pattern_list)

            print("Next best pos " + str((a0, a1)))
            stack = []
            stack.append((a0, a1))

            propogate(self.wave, stack, self.adjacency_information, self.pattern_list)

            return False # returning false continues the loop
        except:
            return False

    def is_solved(self):
        if (self.wave.sum(axis=2) != 1).any():
            return False
        return True
    
    def check_solvable(self):
        if (self.wave.sum(axis=2) == 0).any():
            return False
        return True
    
    def collapse_first_elem(self):
        axis0dim, axis1dim, _ = self.wave.shape
        rand_axis1 = randint(0, axis1dim-1)

        if self.floor:
            rand_axis0 = axis0dim - 1
            possible_floor_patterns = set()
            for key, value in self.adjacency_information.items():
                if len(value["SOUTH"]) == 0:
                    possible_floor_patterns.add(key)
            collapse_to_pattern = random.choice(tuple(possible_floor_patterns))

        else:
            rand_axis0 = randint(0, axis0dim-1)
            collapse_to_pattern = random.choice(list(self.adjacency_information.keys()))

        idx = self.pattern_list.index(collapse_to_pattern)
        self.wave[rand_axis0, rand_axis1, :] = False
        self.wave[rand_axis0, rand_axis1, idx] = True

        stack = []
        stack.append((rand_axis0, rand_axis1))

        propogate(self.wave, stack, self.adjacency_information, self.pattern_list)

def propogate(wave, stack, adjacency_information, pattern_list):
    while len(stack) > 0:
        a0, a1 = stack.pop()
        xdim, ydim, zdim = wave.shape
        sl = wave[a0, a1, :]
        possible_patterns = np.where(sl == True)[0]

        for dir_ in valid_dirs((a0, a1), xdim, ydim):
            adj_sl = wave[a0 + dir_[0], a1 + dir_[1], :]
            adj_possible_patterns = np.where(adj_sl == True)[0]
    
            for adj_pattern in adj_possible_patterns:
                if len(possible_patterns) > 1:
                    is_possible = any(check_possibility(pattern, adj_pattern, adjacency_information, pattern_list, dir_) for pattern in possible_patterns)
                else:
                    is_possible = check_possibility(list(possible_patterns), adj_pattern, adjacency_information, pattern_list, dir_)

                # if this adjacent pattern is not possible for any of the given possible patterns in the current wave
                # then it needs to be set to False
                if not is_possible:
                    adj_pos = (a0 + dir_[0],  a1 + dir_[1])
                    n_a0, n_a1 = adj_pos
                    
                    wave[n_a0, n_a1, adj_pattern] = False

                    if adj_pos not in stack:
                        stack.append(adj_pos)

def check_possibility(pattern, adj_pattern, adj_information, pattern_list, direction):
    if isinstance(pattern, list):
        pattern = pattern[0]
    
    dirs = ["NORTH", "SOUTH", "EAST", "WEST"]
    dims = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    alpha_dir = dirs[dims.index(direction)]
    return pattern_list[adj_pattern] in adj_information[pattern_list[pattern]][alpha_dir]


def valid_dirs(pos, xdim, ydim):
    a0, a1 = pos

    dims = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    valid_dirs = list()
    for dim in dims:
            delta_x, delta_y = dim
            if (a0 + delta_x >= 0) and (a0 + delta_x < xdim):
                if (a1 + delta_y >= 0) and (a1 + delta_y < ydim):
                    valid_dirs.append(dim)
    
    return valid_dirs

    
def observe_next(wave, pattern_list):
    # first, find the element that has the least possible superpositions
    sums = np.sum(wave, axis=2)

    min_elem = sys.maxsize
    min_index_set = set()

    for a0_idx, row in enumerate(sums):
        for a1_idx, elem in enumerate(row):
            if elem < min_elem and elem > 1:
                min_elem = elem
                min_index_set = set()
                min_index_set.add((a0_idx, a1_idx))
            if elem == min_elem:
                min_index_set.add((a0_idx, a1_idx))
    
    min_elem = random.choice(list(min_index_set))

    # within that element, choose a random pattern to collapse to
    min_a0, min_a1 = min_elem
    a2_sl = wave[min_a0, min_a1, :]

    possible_pattern_idxs = list()
    for i, j in enumerate(a2_sl):
        if j:
            possible_pattern_idxs.append(i)

    pattern_idx = random.choice(possible_pattern_idxs)
    
    # then do the actual collapsing
    wave[min_a0, min_a1, :] = False
    wave[min_a0, min_a1, pattern_idx] = True

    return min_a0, min_a1


