class Performace:
    """
    A class to represent performance metrics.
    Attiributes:
        - access_count: Total number of accesses.
        - miss_count: Total number of misses.
        - hit_count: Total number of hits.
    """
    def __init__(self):
        self.access_count = 0
        self.miss_count = 0
        self.hit_count = 0
    
    def record_access(self, hit: bool):
        self.access_count += 1
        if hit:
            self.hit_count += 1
        else:
            self.miss_count += 1
        assert self.access_count == self.hit_count + self.miss_count, "Inconsistent performance metrics"

    def get_miss_rate(self) -> float:
        if self.access_count == 0:
            return 0.0
        return self.miss_count / self.access_count