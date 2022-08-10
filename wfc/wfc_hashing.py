from numpy.typing import NDArray

def hash_pattern_list(pattern_list):
    hash_to_patterns = dict()

    for pattern in pattern_list:
        p_hash = str(pattern.tostring())

        if p_hash not in hash_to_patterns:
            values = list()
            values.append(pattern)

            hash_to_patterns[p_hash] = values
        else:
            current = hash_to_patterns[p_hash]
            current.append(pattern)
            hash_to_patterns[p_hash] = current

    unique_patterns = list(hash_to_patterns.keys())

    new_hash_to_patterns = dict()

    for key, value in hash_to_patterns.items():
        new_hash_to_patterns[key] = value[0]

    return new_hash_to_patterns, unique_patterns

def hash_pattern(pattern: NDArray) -> str:
    return str(pattern.tostring())
