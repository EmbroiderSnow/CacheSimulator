class Line:
    """
    Structure of a cache line.

    Attributes:
        valid: Boolean indicating if the line is valid.
        tag: Tag of the cache line.
        dirty: Boolean indicating if the line has been modified.
    """

    def __init__(self):
        self.valid = False
        self.tag = None
        self.dirty = False
        self.ref_count = 0
        self.access_time = 0
        

    def __repr__(self):
        return (f"Line(valid={self.valid}, tag={self.tag}, "
                f"dirty={self.dirty}, data={self.data})")
    
    def is_valid(self) -> bool:
        return self.valid
    
    def get_tag(self):
        return self.tag
    
    def is_dirty(self) -> bool:
        return self.dirty
    
    def get_data(self, offset):
        """
        Simulate to get data in the line at the specified offset.

        Because we are implementing a cache simulator, the actual data storage is not modeled.

        Args:
            offset: The offset within the cache line.

        Returns:
            Placeholder for data at the specified offset.
        """
        ref_count += 1
        return f"Data at offset {offset} in line with tag {self.tag}"
    
    def fill(self, tag):
        """
        Fill the line with the given tag and mark it as valid.

        Args:
            tag: The tag to set for the line.
        """
        self.tag = tag
        self.valid = True
        self.dirty = False
        self.ref_count = 0

    def set_access_time(self, time):
        """
        Set the access time for the line.

        Args:
            time: The time to set as the access time.
        """
        self.access_time = time