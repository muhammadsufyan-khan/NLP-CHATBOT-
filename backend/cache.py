cache = {}

def get_cache(q):
    return cache.get(q)

def set_cache(q, a):
    cache[q] = a
