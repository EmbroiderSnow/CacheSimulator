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
    
class StreamEntry:
    def __init__(self, start_addr, direction):
        self.monitor_addr = start_addr
        self.last_access = 0
        self.direction = direction

class Stream(PrefetchPolicy):
    def __init__(self, degree=4, table_size=8):
        self.tabel_size = table_size
        self.degree = degree
        self.entries = []
        self.miss_history = set()
        self.history_limit = 16
        self.timestamp = 0

    def on_hit(self, addr, block_size):
        return self.get_prefetch_candidates(addr, block_size)
    
    def on_miss(self, addr, block_size):
        return self.get_prefetch_candidates(addr, block_size)

    def get_prefetch_candidates(self, addr, block_size):
        current_block_addr = (addr // block_size) * block_size
        self.timestamp += 1

        for entry in self.entries:
            dist = current_block_addr - entry.monitor_addr
            if 0 <= dist <= (self.degree * block_size):
                entry.last_access = self.timestamp
                candidates = []
                start_prefetch = current_block_addr + block_size
                for i in range(self.degree):
                    pf_addr = start_prefetch + entry.direction * i * block_size
                    candidates.append(pf_addr)

                entry.monitor_addr = candidates[-1]
                return candidates
            
        prev_block_addr = current_block_addr - block_size
        next_block_addr = current_block_addr + block_size
        if prev_block_addr in self.miss_history:
            new_entry = StreamEntry(current_block_addr, 1)
            self._allocate_entry(new_entry)

            candidates = []
            for i in range(1, self.degree + 1):
                candidates.append(current_block_addr + i * block_size)

            new_entry.monitor_addr = candidates[-1]
            return candidates
        elif next_block_addr in self.miss_history:
            new_entry = StreamEntry(current_block_addr, -1)
            self._allocate_entry(new_entry)

            candidates = []
            for i in range(1, self.degree + 1):
                candidates.append(current_block_addr - i * block_size)

            new_entry.monitor_addr = candidates[-1]
            return candidates
        else:
            self.miss_history.add(current_block_addr)
            if len(self.miss_history) > self.history_limit:
                self.miss_history.pop()
            return []
        
    def _allocate_entry(self, new_entry):
        if len(self.entries) < self.tabel_size:
            self.entries.append(new_entry)
        else:
            evict_index = -1
            oldest_age = 1e18
            for i, entry in enumerate(self.entries):
                if entry.last_access < oldest_age:
                    oldest_age = entry.last_access
                    evict_index = i
            self.entries[evict_index] = new_entry