from enum import Enum
from cache_simulator.controller.performance import Performace
from cache_simulator.controller.memoryHierarchy import MemoryHierarchy

class Status(Enum):
    HIT = "HIT"
    MISS = "MISS"

class MemoryController:
    """
    Control plane for memory hierarchy operations.

    Attributes:
        hierarchy: MemoryHierarchy object representing the memory levels.
        performence: performace metrics of memory operations.
        timestamp: Global clock time for access tracking.
    """
    def __init__(self, file_path):
        self.hierarchy = MemoryHierarchy(file_path)
        self.performence = Performace()
        self.timestamp = 0

    def time_tick(self):
        """
        Increment the global clock time.
        """
        self.timestamp += 1

    def read(self, address):
        """
        Read data from the memory hierarchy starting from L1 cache.

        Args:
            address: The memory address to read from.
        """
        total_latency = 0
        hit_level = -1
        cache_hit = False
        self.time_tick()

        for level, cache in enumerate(self.hierarchy.levels):
            status = cache.read(address)
            self.performence.record_access(status)
            total_latency += cache.hit_latency

            if status == Status.HIT:
                hit_level = level
                cache_hit = True
                break
        
        if not cache_hit:
            total_latency += self.hierarchy.main_memory_latency
            hit_level = len(self.hierarchy.levels)
            total_altency += self.hierarchy.bus_latencies[-1]

        for level in range(hit_level - 1, -1, -1):
            self.hierarchy.levels[level].fill(address)
            total_latency += self.hierarchy.bus_latencies[level]

        self.performence.record_latency(total_latency)