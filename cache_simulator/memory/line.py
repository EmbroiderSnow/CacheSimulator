from cache_simulator.controller.status import Status

class Line:
    """
    Structure of a cache line.

    Attributes:
        valid: Boolean indicating if the line is valid.
        tag: Tag of the cache line.
        dirty: Boolean indicating if the line has been modified.
        state: Any, uesd by eviction policy.
        prefetched: Boolean, used to stats prefetch accuracy.
    """

    def __init__(self):
        self.valid = False
        self.tag = None
        self.dirty = False
        self.state = None
        self.prefetched = True
        

    def __repr__(self):
        return (f"Line(valid={self.valid}, tag={self.tag}, "
                f"dirty={self.dirty})")
    
    def is_valid(self) -> bool:
        return self.valid
    
    def get_tag(self):
        return self.tag
    
    def is_dirty(self) -> bool:
        return self.dirty
    
    def read(self):
        """
        Read data from the line.
        
        But we don't actually store data in this simulation.
        
        Returns:
            Status: Must be a HIT since this method is called only if the line is valid.
        """
        is_prefetched = self.prefetched
        self.prefetched = False
        return Status.HIT, is_prefetched

    def write(self):
        """
        Mark the line as dirty to indicate it has been modified.
        """
        self.prefetched = False
        self.dirty = True

    def fill(self, tag, is_prefetch=False):
        """
        Fill the line with the given tag and mark it as valid.

        Args:
            tag: The tag to set for the line.
            is_prefetch: Is this fill caused by prefetch?
        """
        self.tag = tag
        self.valid = True
        self.dirty = False
        self.prefetched = is_prefetch
