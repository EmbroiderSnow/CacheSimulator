from set import Set

cache_structure = []

class Cache:
    """
    Structure of a cache.

    It can describe various levels of cache (L1, L2, L3) with different configurations.
    
    Attributes:
        cache_size: Total size of the cache in bytes.
        block_size: Size of each block in bytes.
        associativity: Number of lines per set.
        level: Cache level (e.g., L1, L2).
        eviction_policy: Policy used for evicting cache lines (e.g., LRU, FIFO).
        sets: List of Set objects.
    """
    
    def __init__(self, cache_size, block_size, associativity, level, eviction_policy):
        self.cache_size = cache_size
        self.block_size = block_size
        self.associativity = associativity
        self.level = level
        self.eviction_policy = eviction_policy
        self.sets = [Set() for _ in range(self.cache_size // (self.block_size * self.associativity))]

    def __repr__(self):
        return (f"Cache(level={self.level}, size={self.cache_size}B, block_size={self.block_size}B, "
                f"associativity={self.associativity}, eviction_policy={self.eviction_policy})")
    
    def get_number_of_sets(self):
        return len(self.sets)
    
    def get_associativity(self):
        return self.associativity
    
    def get_block_size(self):
        return self.block_size
    
    def get_cache_size(self):
        return self.cache_size
    
    def get_eviction_policy(self):
        return self.eviction_policy
    
    def get_level(self):
        return self.level
    
    def read_data(self, address):
        # Placeholder for read operation
        pass

    def write_data(self, address, data):
        # Placeholder for write operation
        pass

        