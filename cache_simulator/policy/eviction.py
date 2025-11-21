from cache_simulator.memory.line import Line
    
class EvictionPolicy:
    """
    Base class for eviction policies.

    Methods:
        evict(set): Evict a line from the given set based on the policy.
        update_on_access(set, line): Update the policy state when a line is accessed.
    """

    def evict(self, cache_set) -> Line:
        raise NotImplementedError("Evict method must be implemented by subclasses.")

    def update_on_access(self, cache_set, line):
        raise NotImplementedError("Update on access method must be implemented by subclasses.")
    
class LRU(EvictionPolicy):
    """
    Least Recently Used (LRU) eviction policy implementation.
    """

    def evict(self, cache_set) -> Line:
        min_index = 0
        min_time = int(1e18)
        for i, line in enumerate(cache_set.lines):
            timestamp = line.state if line.state is not None else 0
            if timestamp < min_time:
                min_time = timestamp
                min_index = i
        return cache_set.lines[min_index]

    def update_on_access(self, cache_set, line, timestamp):
        line.state = timestamp

    def on_fill(self, cache_set, line, timestamp):
        line.state = timestamp

class SRRIP(EvictionPolicy):
    """
    Static Re-reference Interval Prediction
    """
    pass