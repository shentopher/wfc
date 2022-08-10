from wfc_hashing import hash_pattern
"""
@params: pattern_catalog, which has (x, y) as key and NDArray pattern as value
@returns: adjacency_information, dictionary
    key is hashed pattern
    value is a dictionary with four keys: North, South, East, West. The value for each key is a set of adjacent patterns
"""
def get_adjacencies(pattern_catalog, xtiles, ytiles):
    adjacency_information = dict()

    for key, pattern in pattern_catalog.items():
        x, y = key

        pattern = hash_pattern(pattern)

        NORTH = ("NORTH", None)
        SOUTH = ("SOUTH", None)
        EAST = ("EAST", None)
        WEST = ("WEST", None)
        
        if x - 1 >= 0:
            N_CORD = (x - 1, y)
            NORTH = ("NORTH", hash_pattern(pattern_catalog[N_CORD]))
        if x + 1 < ytiles:
            S_CORD = (x + 1, y)
            SOUTH = ("SOUTH", hash_pattern(pattern_catalog[S_CORD]))
        if y - 1 >= 0:
            E_CORD = (x, y - 1)
            EAST = ("EAST", hash_pattern(pattern_catalog[E_CORD]))
        if y + 1 < xtiles:
            W_CORD = (x, y + 1)
            WEST = ("WEST", hash_pattern(pattern_catalog[W_CORD]))

        directions = [NORTH, SOUTH, EAST, WEST]

        if pattern in adjacency_information.keys():
            pattern_information = adjacency_information[pattern]
            for direction, adj_pattern in directions:
                if adj_pattern is not None:
                    adjacencies = pattern_information[direction]
                    adjacencies.add(adj_pattern)
                    pattern_information.update({direction : adjacencies})
            adjacency_information[pattern] = pattern_information

        else:
            pattern_information = dict()
            for direction, adj_pattern in directions:
                adjs = set()

                if adj_pattern is not None:
                    adjs.add(adj_pattern)
                pattern_information[direction] = adjs

            adjacency_information[pattern] = pattern_information
        
    return adjacency_information


def make_adj(adjacency_information, pattern_list):
    # preprocessing
    direction_dict = {
        "NORTH" : (-1, 0),
        "SOUTH" : (1, 0),
        "WEST" : (0, -1),
        "EAST" : (0, 1)
    }

    adjacency_relations = list()

    for pattern1, value in adjacency_information.items():
        for direction, patterns in value.items():
            for pattern2 in patterns:
                pdir = direction_dict.get(direction)
                pattern1_idx = pattern_list.index(pattern1)
                pattern2_idx = pattern_list.index(pattern2)
                
                adjacency_relations.append((pdir, pattern1_idx, pattern2_idx))
    
    # more preprocessing

    adjacency_list = list()

    for direction, _ in direction_dict.items():
        adjacency_list[direction] = [set() for _ in pattern_list]
    
    for adjacency, pattern1_idx, pattern2_idx in adjacency_relations:
        adjacency_list[adjacency][pattern1_idx].add(pattern2_idx)
    
    # The adjacency matrix is a boolean matrix, indexed by the direction and the two patterns.
    # If the value for (direction, pattern1, pattern2) is True, then this is a valid adjacency.

    
