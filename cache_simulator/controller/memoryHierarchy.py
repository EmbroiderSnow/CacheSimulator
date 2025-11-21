import json
from cache_simulator.memory.cache import Cache

class MemoryHierarchy:
    """
    Structure to represent the memory hierarchy levels.
    
    Attributes:
        levels: List of Caches (e.g., L1, L2, L3).
        bus_latencies: List of bus latencies between levels.
        main_memory_latency: Latency of the main memory.
    """

    def __init__(self, file_path):
        """
        Initializes the memory hierarchy from a JSON configuration file.
        """
        with open(file_path, 'r') as f:
            config = json.load(f)

        self.cache_hierarchy = config["cache_hierarchy"]
        self.levels = []
        for cache_config in self.cache_hierarchy:
            prefetch_config = cache_config["config"].get("prefetch", None)
            bypass_config = cache_config["config"].get("bypass", None)
            cache = Cache(
                name=cache_config["id"],
                cache_size=cache_config["config"]["size"],
                block_size=cache_config["config"]["block_size"],
                associativity=cache_config["config"]["associativity"],
                level=cache_config["level"],
                hit_latency=cache_config["config"]["hit_latency"],
                eviction_policy=cache_config["config"]["replacement_policy"],
                prefetch=prefetch_config,
                bypass=bypass_config,
                write_policy=cache_config["config"]["write_policy"],
                write_allocate=cache_config["config"]["allocation_policy"]
            )
            self.levels.append(cache)
        self.interconnects = config["interconnects"]
        self.bus_latencies = [interconnect["bus_latency"] for interconnect in self.interconnects]
        self.main_memory_latency = config["main_memory"]["access_latency"]