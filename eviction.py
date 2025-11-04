from cache import Cache
from set import Set
from line import Line

def EvictionPolicyFactory(policy_name):
    """
    Factory function to create eviction policy instances based on the policy name.

    Args:
        policy_name (str): Name of the eviction policy (e.g., 'LRU', 'FIFO').

    Returns:
        EvictionPolicy: An instance of the corresponding eviction policy class.
    """
    if policy_name == 'LRU':
        # return LRU()
        pass
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
        # Implement LRU eviction logic
        pass

    def update_on_access(self, cache_set, line):
        # Implement LRU update logic on access
        pass
