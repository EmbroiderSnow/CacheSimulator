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

    def __init__(self, index, associativity, block_size, eviction_plicy: EvictionPolicy):
        self.index = index
        self.associativity = associativity
        self.block_size = block_size
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
    
    def fill_line(self, tag, timestamp) -> tuple:
        """
        Fills a line in the set with the given tag.
        
        Args:
            tag: The tag of the line to fill.
            timestamp: The current global clock time.

        Returns:
            tuple: (is_dirty_evicted: bool, evicted_line_address: int)
        """
        for line in self.lines:
            if not line.is_valid():
                line.fill(tag)
                line.set_access_time(timestamp)
                return (False, 0)
        # Fall into eviction policy if no empty line is found
        evicted_line = self.eviction_policy.evict(self)
        evicted_line.set_access_time(timestamp)
        evicted_line.fill(tag)
        if evicted_line.is_dirty():
            evicted_line.dirty = False
            return (True, self.get_address_of_line(evicted_line))
        else :
            return (False, 0)
        
    def get_address_of_line(self, line: Line) -> int:
        """
        Get the full address of a given line in the set.

        Args:
            line (Line): The line whose address is to be computed.

        Returns:
            int: The full address corresponding to the line.
        """
        tag = line.get_tag()
        index = self.index
        offset = 0  # Assuming offset is 0 for the start of the block
        address = (tag << (self.index.bit_length() + self.block_size.bit_length())) | (index << self.block_size.bit_length()) | offset
        return address
        