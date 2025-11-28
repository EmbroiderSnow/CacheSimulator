from cache_simulator.controller.performance import Performance
from cache_simulator.controller.memoryHierarchy import MemoryHierarchy
from cache_simulator.controller.status import Status

class MemoryController:
    """
    Control plane for memory hierarchy operations.

    Attributes:
        hierarchy: MemoryHierarchy object representing the memory levels.
        performance: performance metrics of memory operations.
        timestamp: Global clock time for access tracking.
    """
    def __init__(self, file_path):
        self.hierarchy = MemoryHierarchy(file_path)
        self.performance = Performance()
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
            status = cache.read(address, self.timestamp)
            if level == 0:
                self.performance.record_access(status)
            self.performance.record_cache_access(cache.name, status)
            total_latency += cache.hit_latency

            if status == Status.HIT:
                hit_level = level
                cache_hit = True
                break
        
        if not cache_hit:
            total_latency += self.hierarchy.main_memory_latency
            hit_level = len(self.hierarchy.levels)
            self.performance.record_cache_access("MainMemory", None)
            total_latency += self.hierarchy.bus_latencies[-1]

        for level in range(hit_level - 1, -1, -1):
            is_dirty, evited, evicted_address, _ = self.hierarchy.levels[level].fill(address, self.timestamp)
            total_latency += self.hierarchy.bus_latencies[level]
            if evited:
                self.performance.record_replacement()
            if is_dirty:
                # write back to next level
                self.handle_write_back(evicted_address, level + 1, sync=False)

        self.performance.record_latency(total_latency)

    def write(self, address):
        """
        Write data to L1 cache in the memory hierarchy.
        
        Args:
            address: The memory address to write to.
        """
        self.performance.record_latency(self.hierarchy.levels[0].hit_latency)
        self.handle_write_back(address, 0, sync=True)

    def handle_write_back(self, address, level, sync: bool):
        """
        Handle write-back operation for an address.

        A write-back to cache level in memory hierarchy with level "level".
        
        Args:
            address: The memory address to write back.
            level: The cache level where the write-back needs to be written into.
            sync: If True, perform synchronous write-back; else asynchronous.
        """
        if level >= len(self.hierarchy.levels):
            return
        
        if sync:
            self.time_tick()

        cache = self.hierarchy.levels[level]
        status = cache.write(address, self.timestamp)
        self.performance.record_cache_access(cache.name, status)

        if sync:
            self.performance.record_access(status)

        if status == Status.MISS:
            hit_level = -1
            cache_hit = False

            for lvl in range(level + 1, len(self.hierarchy.levels)):
                cur_cache = self.hierarchy.levels[lvl]
                status = cur_cache.read(address, self.timestamp)
                self.performance.record_cache_access(cur_cache.name, status)
                if status == Status.HIT:
                    hit_level = lvl
                    cache_hit = True
                    break

            if not cache_hit:
                hit_level = len(self.hierarchy.levels)
                self.performance.record_cache_access("MainMemory", None)

            for lvl in range(hit_level - 1, level - 1, -1):
                is_dirty, evicted, evicted_address, _ = self.hierarchy.levels[lvl].fill(address, self.timestamp)
                self.performance.record_latency(self.hierarchy.levels[lvl].hit_latency)
                if evicted:
                    self.performance.record_replacement()
                if is_dirty:
                    self.handle_write_back(evicted_address, lvl + 1, sync=False)

            # Now the line is in the cache at 'level', perform the write
            s = cache.write(address, self.timestamp)
            self.performance.record_cache_access(cache.name, s)

    def collect_prefetch_information(self):
        for cache in self.hierarchy.levels:
            self.performance.prefetch_count += cache.prefetch_count
            self.performance.prefetch_miss_count += cache.prefetch_miss_count
    
    def calculate_AMAT(self, level: int) -> float:
        """
        Calculate the Average Memory Access Time (AMAT) up to a specified cache level.

        Args:
            level: The cache level up to which AMAT is calculated (0-indexed).

        Returns:
            The calculated AMAT as a float.
        """
        amat = 0.0
        miss_rate = self.performance.get_miss_rate(self.hierarchy.levels[level].name)
        print(f"Level {level} Miss Rate: {miss_rate:.4f}")
        amat = self.hierarchy.levels[level].hit_latency + miss_rate * (
            self.hierarchy.bus_latencies[level] + 
            (self.calculate_AMAT(level + 1) if level + 1 < len(self.hierarchy.levels) else self.hierarchy.main_memory_latency)
        )
        self.performance.amat[self.hierarchy.levels[level].name] = amat
        return amat
        