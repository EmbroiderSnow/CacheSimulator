from cache_simulator.memory.line import Line
from cache_simulator.controller.control import clock_time

class Set:
    """
    Structure of a cache set.

    Attributes:
        lines: List of Line objects in the set.
        associativity: Number of lines per set.
        eviction_policy: Eviction policy applied to this set.
    """

    def __init__(self, associativity, eviction_plicy):
        self.associativity = associativity
        self.eviction_policy = eviction_plicy
        self.lines = [Line() for _ in range(associativity)]

    def __repr__(self):
        return f"Set(associativity={self.associativity}, lines={self.lines})"
    
    def read_line(self, tag, offset):
        """
        Reads a line from the set based on the tag and offset.

        Args:
            tag: The tag of the line to read.
            offset: The offset within the line.
        
        Returns:
            The data at the specified offset if the line is found, else None.
        """
        for line in self.lines:
            if line.is_valid() and line.get_tag() == tag:
                return line.get_data(offset)
        return None
    
    def fill_line(self, tag):
        """
        Fills a line in the set with the given tag.
        
        Args:
            tag: The tag of the line to fill.
        """
        for line in self.lines:
            if not line.is_valid():
                line.fill(tag)
                line.set_access_time(clock_time)
                return 
        # Fall into eviction policy if no empty line is found
        evicted_line = self.eviction_policy.evict(self)
        self.eviction_policy.update_on_access(self, evicted_line)
        evicted_line.fill(tag)
        