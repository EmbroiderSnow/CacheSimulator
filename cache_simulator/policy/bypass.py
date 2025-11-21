import random
random.seed(0)

class BypassPolicy:
    """
    Bypass policy base class.
    """
    def should_bypass(self, cache_set, is_prefetch) -> bool:
        """
        Decide fill the cache line or not.
        """
        raise NotImplementedError("Should bypass must be implemented in subclass")
    
class NoBypass(BypassPolicy):
    """
    Never bypass, fill all data.
    """
    def should_bypass(self, cache_set, is_prefetch):
        return False
    
class ProbBypass(BypassPolicy):
    """
    Probabilistic bypass policy.
    """

    def __init__(self, bypass_prob_demand=0.01, bypass_prob_prefetch=0.20):
        self.prob_demand = bypass_prob_demand
        self.prob_prefetch = bypass_prob_prefetch

    def should_bypass(self, cache_set, is_prefetch):
        if not cache_set.is_full():
            return False
        
        threshold = self.prob_prefetch if is_prefetch else self.prob_demand
        return random.random() < threshold