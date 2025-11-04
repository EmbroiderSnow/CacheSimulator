from line import Line

class Set:
    """
    Structure of a cache set.

    Attributes:
        lines: List of Line objects in the set.
        associativity: Number of lines per set.
    """

    def __init__(self, associativity):
        self.associativity = associativity
        self.lines = [Line() for _ in range(associativity)]