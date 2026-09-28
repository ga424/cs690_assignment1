from collections import Counter

def top_k_frequent(items, k):
    if k == 0:
        return []
    counts = Counter(items)
    first_index = {}
    for index, item in enumerate(items):
        if item not in first_index:
            first_index[item] = index
    return sorted(counts, key=lambda item: (-counts[item], first_index[item]))[:k]
