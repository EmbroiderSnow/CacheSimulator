class PrefetchPolicy:
    def __init__(self, degree=1):
        self.degree = degree

    def on_miss(self, addr, block_size):
        raise NotImplementedError("On miss must be implemented in subclass")
    
    def on_hit(self, addr, block_size):
        raise NotImplementedError("On hit must be implemented in subclass")

    def get_prefetch_candidates(self, addr, block_size) -> list:
        """
        Based on the addr and block_size, return list of the address need to be prefetched.
        """
        return []
    
class NoPrefetch(PrefetchPolicy):
    """
    Do not prefetch.
    """
    
    def on_miss(self, addr, block_size):
        return []
    
    def on_hit(self, addr, block_size):
        return []
    
    def get_prefetch_candidates(self, addr, block_size):
        return super().get_prefetch_candidates(addr, block_size)

class NexNLine(PrefetchPolicy):
    """
    Prefetch next n blocks, n defined as degree.
    """

    def on_miss(self, addr, block_size):
        return self.get_prefetch_candidates(addr, block_size)
        
    def on_hit(self, addr, block_size):
        return []

    def get_prefetch_candidates(self, addr, block_size):
        candidates = []
        current_block_addr = (addr // block_size) * block_size

        for i in range(1, self.degree + 1):
            prefetch_addr = current_block_addr + (i * block_size)
            candidates.append(prefetch_addr)
        
        return candidates
    