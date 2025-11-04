class Line:
    """
    Structure of a cache line.

    Attributes:
        valid: Boolean indicating if the line is valid.
        tag: Tag of the cache line.
        dirty: Boolean indicating if the line has been modified.
        data: Data stored in the cache line.
    """

    def __init__(self):
        self.valid = False
        self.tag = None
        self.dirty = False
        self.data = None
