import json
from enum import Enum

clock_time = 0

class Status(Enum):
    HIT = "HIT"
    MISS = "MISS"

class MemoryHierarchy:
    """
    Structure to represent the memory hierarchy levels.
    
    Attributes:
        levels: List of memory levels (e.g., L1, L2, L3, Main Memory).
    """

    def __init__(self, file_path):
        """
        Initializes the memory hierarchy from a JSON configuration file.
        """
        pass