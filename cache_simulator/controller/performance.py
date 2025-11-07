from cache_simulator.controller.control import Status

class Performace:
    """
    A class to represent performance metrics.
    
    Attiributes:
        access_count: Total number of accesses.
        miss_count: Total number of misses.
        hit_count: Total number of hits.
        total_latency: Total latency of all accesses.
    """
    def __init__(self):
        self.access_count = 0
        self.miss_count = 0
        self.hit_count = 0
        self.total_latency = 0
    
    def record_access(self, hit: Status):
        self.access_count += 1
        if hit == Status.HIT:
            self.hit_count += 1
        else:
            self.miss_count += 1
        assert self.access_count == self.hit_count + self.miss_count, "Inconsistent performance metrics"

    def record_latency(self, latency: int):
        self.total_latency += latency

    def get_miss_rate(self) -> float:
        if self.access_count == 0:
            return 0.0
        return self.miss_count / self.access_count