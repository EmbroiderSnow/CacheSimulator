from cache_simulator.memory.set import Set
from cache_simulator.controller.status import Status
from cache_simulator.policy.evictionPolicyFactory import EvictionPolicyFactory

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
        write_policy: Policy used for writing data (e.g., write-back, write-through).
        allocate_policy: Policy for allocating on write misses (e.g., write-allocate, no-write-allocate).
        sets: List of Set objects.
    """

    def __init__(self, name, cache_size, block_size, associativity, level, hit_latency, eviction_policy, write_policy, write_allocate):
        self.name = name
        self.cache_size = self.parse_size_to_bytes(cache_size)
        self.block_size = block_size
        self.associativity = associativity
        self.level = level
        self.hit_latency = hit_latency
        self.eviction_policy = EvictionPolicyFactory(eviction_policy)
        self.write_policy = write_policy
        self.allocate_policy = write_allocate
        self.set_num = self.cache_size // (block_size * associativity)
        self.sets = [Set(index=i, associativity=associativity, block_size=block_size, eviction_plicy=self.eviction_policy) for i in range(self.set_num)]
        

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
        return target_set.read_line(tag, timestamp)
    
    def write(self, address, timestamp) -> Status:
        tag, index, offset = self.parse_address(address)
        target_set = self.sets[index]
        return target_set.write_line(tag, timestamp)

    def fill(self, address, timestamp) -> tuple:
        tag, index, offset = self.parse_address(address)
        target_set = self.sets[index]
        return target_set.fill_line(tag, timestamp)

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
        index = (address >> self.block_size.bit_length()) & mask_index
        tag = address >> (self.block_size.bit_length() + self.set_num.bit_length())
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