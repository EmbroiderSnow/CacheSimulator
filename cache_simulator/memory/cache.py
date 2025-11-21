import math
from cache_simulator.memory.set import Set
from cache_simulator.controller.status import Status
from cache_simulator.policy.evictionPolicyFactory import EvictionPolicyFactory
from cache_simulator.policy.prefetchPolicyFactory import PrefetchPolicyFactory

class Cache:
    """
    Structure of a cache.

    It can describe various levels of cache (L1, L2, L3) with different configurations.
    
    Attributes:
        name: Name of the cache.
        cache_size: Total size of the cache in bytes.
        block_size: Size of each block in bytes.
        associativity: Number of lines per set.
        level: Cache level (e.g., L1, L2).
        hit_latency: Latency for a cache hit in cycles.
        eviction_policy: Policy used for evicting cache lines (e.g., LRU, FIFO).
        prefetch_policy: Policy used for prefetch data(e.g., NextNLine, Stream, Stride).
        prefetch_degree: Argument used for prefetch policy.
        write_policy: Policy used for writing data (e.g., write-back, write-through).
        allocate_policy: Policy for allocating on write misses (e.g., write-allocate, no-write-allocate).
        sets: List of Set objects.
    """

    def __init__(self, name, cache_size, block_size, associativity, level, hit_latency, eviction_policy, prefetch_policy, prefetch_degree, write_policy, write_allocate):
        self.name = name
        self.cache_size = self.parse_size_to_bytes(cache_size)
        self.block_size = block_size
        self.associativity = associativity
        self.level = level
        self.hit_latency = hit_latency
        self.eviction_policy = EvictionPolicyFactory(eviction_policy)
        self.prefetch_policy = PrefetchPolicyFactory(prefetch_policy, prefetch_degree)
        self.write_policy = write_policy
        self.allocate_policy = write_allocate
        self.set_num = self.cache_size // (block_size * associativity)
        self.offset_bits = int(math.log2(block_size))
        self.index_bits = int(math.log2(self.set_num))
        self.sets = [Set(index=i, associativity=associativity, block_size=block_size, eviction_plicy=self.eviction_policy, offset_bits=self.offset_bits, index_bits=self.index_bits) for i in range(self.set_num)]

        self.prefetch_count = 0
        self.prefetch_miss_count = 0
        

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
    
    def read(self, address, timestamp) -> Status:
        tag, index, offset = self.parse_address(address)
        target_set: Set = self.sets[index]
        status = target_set.read_line(tag, timestamp)
        if status == Status.MISS:
            self.handle_prefetch(address, timestamp)
        return status
    
    def write(self, address, timestamp) -> Status:
        tag, index, offset = self.parse_address(address)
        target_set = self.sets[index]
        return target_set.write_line(tag, timestamp)

    def fill(self, address, timestamp) -> tuple:
        tag, index, offset = self.parse_address(address)
        target_set = self.sets[index]
        ret = target_set.fill_line(tag, timestamp)
        if ret[3]:
            self.prefetch_miss_count += 1
        return ret

    def parse_address(self, address):
        """
        Parse the given address into tag, index, and offset components.

        Args:
            address (int): The memory address to parse.

        Returns:
            tuple: A tuple containing (tag, index, offset).
        """
        # Placeholder for address parsing logic
        mask_offset = self.block_size - 1
        mask_index = self.set_num - 1
        offset = address & mask_offset
        index = (address >> self.offset_bits) & mask_index
        tag = address >> (self.offset_bits + self.index_bits)
        return tag, index, offset
        
    def parse_size_to_bytes(self, size_str):
        """
        Parse strings like "32KB", "256MB", "8GB" and return the corresponding size in bytes.
        """
        size_str = size_str.strip().upper()
        
        multipliers = {
            'B': 1,
            'KB': 1024,
            'MB': 1024**2,
            'GB': 1024**3,
        }

        num_str = ""
        unit_str = ""
        for i, char in enumerate(size_str):
            if not char.isdigit():
                num_str = size_str[:i]
                unit_str = size_str[i:]
                break
        
        if not unit_str:
            num_str = size_str
            unit_str = 'B'

        unit_str = unit_str.strip()

        try:
            number = int(num_str)
        except ValueError:
            raise ValueError(f"Invalid number '{num_str}' in size string: '{size_str}'")

        if unit_str not in multipliers:
            raise ValueError(f"Invalid unit '{unit_str}' in size string: '{size_str}'")

        return number * multipliers[unit_str]
    
    def handle_prefetch(self, address, timestamp):
        candidates = self.prefetch_policy.get_prefetch_candidates(address, self.block_size)
        for prefetch_addr in candidates:
            self.fill_prefetch(prefetch_addr, timestamp)

    def fill_prefetch(self, address, timestamp):
        """
        Returns:
            True if count this prefetch(prefetch target address not in Set)
            False if not count this prefetch(prefetch target already in Set)
        """
        tag, index, offset = self.parse_address(address)
        target_set = self.sets[index]
        if not target_set.contain_tag(tag):
            self.prefetch_count += 1
            target_set.fill_line(tag, timestamp, is_prefetch=True)