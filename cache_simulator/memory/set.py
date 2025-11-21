from cache_simulator.memory.line import Line
from cache_simulator.controller.status import Status
from cache_simulator.policy.eviction import EvictionPolicy

class Set:
    """
    Structure of a cache set.

    Attributes:
        lines: List of Line objects in the set.
        associativity: Number of lines per set.
        eviction_policy: Eviction policy applied to this set.
        offset_bits: Number of bits for block offset.
        index_bits: Number of bits for set index.
    """

    def __init__(self, index, associativity, block_size, eviction_plicy: EvictionPolicy, offset_bits, index_bits):
        self.index = index
        self.associativity = associativity
        self.block_size = block_size
        self.eviction_policy = eviction_plicy
        self.offset_bits = offset_bits
        self.index_bits = index_bits
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
                self.eviction_policy.update_on_access(self, line, timestamp=timestamp);
                return line.read()
        return Status.MISS, None
    
    def write_line(self, tag, timestamp) -> Status:
        """
        Writes to a line in the set based on the tag.

        Args:
            tag: The tag of the line to write.
            timestamp: The current global clock time.
        """
        for line in self.lines:
            if line.is_valid() and line.get_tag() == tag:
                self.eviction_policy.update_on_access(self, line, timestamp=timestamp);
                line.write()
                return Status.HIT
        return Status.MISS
    
    def fill_line(self, tag, timestamp, is_prefetch=False) -> tuple:
        """
        Fills a line in the set with the given tag.
        
        Args:
            tag: The tag of the line to fill.
            timestamp: The current global clock time.
            is_prefetch: Is this fill caused by prefetch?

        Returns:
            tuple: (is_dirty: bool, evicted: bool, evicted_line_address: int, prefetch_miss: bool)
        """
        for line in self.lines:
            if not line.is_valid():
                line.fill(tag, is_prefetch)
                self.eviction_policy.on_fill(self, line, timestamp=timestamp)
                return (False, False, 0, 0)
        # Fall into eviction policy if no empty line is found
        evicted_line = self.eviction_policy.evict(self)
        prefetch_miss = evicted_line.prefetched
        evicted_address = self.get_address_of_line(evicted_line)
        self.eviction_policy.on_fill(self, evicted_line, timestamp=timestamp)
        evicted_line.fill(tag, is_prefetch)
        if evicted_line.is_dirty():
            evicted_line.dirty = False
            return (True, True, evicted_address, prefetch_miss)
        else:
            return (False, True, 0, prefetch_miss)
        
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
        address = (tag << (self.index_bits + self.offset_bits)) + \
                  (index << self.offset_bits) + offset
        return address
        
    def contain_tag(self, tag) -> bool:
        for line in self.lines:
            if line.tag == tag:
                return True
        return False
    
    def is_full(self):
        for line in self.lines:
            if not line.is_valid():
                return False
        return True
    
    def get_line(self, tag):
        for line in self.lines:
            if line.get_tag() == tag:
                return line
        return None