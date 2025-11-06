from cache_simulator.memory.cache import Cache
from cache_simulator.memory.set import Set
from cache_simulator.memory.line import Line
from cache_simulator.controller.control import clock_time

def EvictionPolicyFactory(policy_name):
    """
    Factory function to create eviction policy instances based on the policy name.

    Args:
        policy_name (str): Name of the eviction policy (e.g., 'LRU', 'FIFO').

    Returns:
        EvictionPolicy: An instance of the corresponding eviction policy class.
    """
    if policy_name == 'LRU':
        return LRU()
    elif policy_name == 'FIFO':
        # return FIFO()
        pass
    else:
        raise ValueError(f"Unknown eviction policy: {policy_name}")
    
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
            if line.access_time < min_time:
                min_time = line.access_time
                min_index = i
        return cache_set.lines[min_index]


    def update_on_access(self, cache_set, line):
        line.set_access_time(clock_time)
