from cache_simulator.controller.status import Status

class Performance:
    """
    A class to represent performance metrics.
    
    Attiributes:
        access_count: Total number of accesses.
        miss_count: Total number of misses.
        hit_count: Total number of hits.
        total_latency: Total latency of all accesses.
        cache_access_count: Dictionary mapping cache levels to their access counts.
        replacement_count: Number of replacements made.
    """
    def __init__(self):
        self.access_count = 0
        self.miss_count = 0
        self.hit_count = 0
        self.total_latency = 0
        self.cache_access_count = {}
        self.replacement_count = 0
        self.prefetch_count = 0
        self.prefetch_miss_count = 0
    
    def record_access(self, hit: Status):
        self.access_count += 1
        if hit == Status.HIT:
            self.hit_count += 1
        else:
            self.miss_count += 1
        assert self.access_count == self.hit_count + self.miss_count, "Inconsistent performance metrics"

    def record_cache_access(self, level_id: str):
        if level_id not in self.cache_access_count:
            self.cache_access_count[level_id] = 0
        self.cache_access_count[level_id] += 1

    def record_replacement(self):
        self.replacement_count += 1

    def record_latency(self, latency: int):
        self.total_latency += latency

    def get_miss_rate(self) -> float:
        if self.access_count == 0:
            return 0.0
        return self.miss_count / self.access_count
    
    def print_stats(self):
        print("Performance Statistics:")
        print(f"Total Accesses: {self.access_count}")
        print(f"Total Hits: {self.hit_count}")
        print(f"Total Misses: {self.miss_count}")
        print(f"Miss Rate: {self.get_miss_rate()*100:.2f}%")
        print(f"Total Latency: {self.total_latency} cycles")
        print(f"Average Latency per Access: {self.total_latency / self.access_count if self.access_count > 0 else 0:.2f} cycles")
        print("Cache Access Counts:")
        for level_id, count in self.cache_access_count.items():
            print(f"  {level_id}: {count} accesses")
        print(f"Prefetch count: {self.prefetch_count}")
        print(f"Prefetch miss count: {self.prefetch_miss_count}")
        print(f"Total Replacements: {self.replacement_count}")