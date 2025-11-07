from cache_simulator.memory.line import Line
from cache_simulator.controller.control import clock_time, Status
from cache_simulator.policy.eviction import EvictionPolicy

class Set:
    """
    Structure of a cache set.

    Attributes:
        lines: List of Line objects in the set.
        associativity: Number of lines per set.
        eviction_policy: Eviction policy applied to this set.
    """

    def __init__(self, associativity, eviction_plicy: EvictionPolicy):
        self.associativity = associativity
        self.eviction_policy = eviction_plicy
        self.lines = [Line() for _ in range(associativity)]

    def __repr__(self):
        return f"Set(associativity={self.associativity}, lines={self.lines})"
    
    def read_line(self, tag, timestamp) -> Status:
        """
        Reads a line from the set based on the tag and offset.

        Args:
            tag: The tag of the line to read.
            offset: The offset within the line.
            timestamp: The current global clock time.
        
        Returns:
            The data at the specified offset if the line is found, else None.
        """
        for line in self.lines:
            if line.is_valid() and line.get_tag() == tag:
                line.set_access_time(timestamp)
                return line.read()
        return Status.MISS
    
    def write_line(self, tag, timestamp) -> Status:
        """
        Writes to a line in the set based on the tag.

        Args:
            tag: The tag of the line to write.
            timestamp: The current global clock time.
        """
        for line in self.lines:
            if line.is_valid() and line.get_tag() == tag:
                line.set_access_time(timestamp)
                line.write()
                return Status.HIT
        return Status.MISS
    
    def fill_line(self, tag, timestamp):
        """
        Fills a line in the set with the given tag.
        
        Args:
            tag: The tag of the line to fill.
            timestamp: The current global clock time.
        """
        for line in self.lines:
            if not line.is_valid():
                line.fill(tag)
                line.set_access_time(timestamp)
                return 
        # Fall into eviction policy if no empty line is found
        evicted_line = self.eviction_policy.evict(self)
        self.eviction_policy.update_on_access(self, evicted_line)
        evicted_line.fill(tag)
        