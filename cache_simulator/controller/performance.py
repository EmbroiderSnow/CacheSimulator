import os
import json
from cache_simulator.controller.status import Status

# ANSI color codes for terminal output
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BLUE = "\033[94m"

class Performance:
    """
    A class to represent performance metrics.
    
    Attributes:
        access_count: Total number of accesses.
        miss_count: Total number of misses.
        hit_count: Total number of hits.
        total_latency: Total latency of all accesses.
        cache_access_count: Dictionary mapping cache levels to their access counts.
        replacement_count: Number of replacements made.
    """
    def __init__(self):
        self.access_count = 0
        self.miss_count = 0
        self.hit_count = 0
        self.total_latency = 0
        self.cache_access_count = {}
        self.replacement_count = 0
        self.prefetch_count = 0
        self.prefetch_miss_count = 0
    
    def record_access(self, hit: Status):
        self.access_count += 1
        if hit == Status.HIT:
            self.hit_count += 1
        else:
            self.miss_count += 1
        assert self.access_count == self.hit_count + self.miss_count, "Inconsistent performance metrics"

    def record_cache_access(self, level_id: str):
        if level_id not in self.cache_access_count:
            self.cache_access_count[level_id] = 0
        self.cache_access_count[level_id] += 1

    def record_replacement(self):
        self.replacement_count += 1

    def record_latency(self, latency: int):
        self.total_latency += latency

    def get_miss_rate(self) -> float:
        if self.access_count == 0:
            return 0.0
        return self.miss_count / self.access_count

    def _get_formatted_stats(self, config_data=None, use_color=False) -> str:
        """
        Helper function to format statistics for both terminal and file output.
        """
        # Color definitions
        c_title = BOLD + CYAN if use_color else ""
        c_header = BOLD + BLUE if use_color else ""
        c_label = BOLD if use_color else ""
        c_val = GREEN if use_color else ""
        c_warn = RED if use_color else ""
        c_reset = RESET if use_color else ""

        lines = []
        lines.append(f"{c_title}========================================{c_reset}")
        lines.append(f"{c_title}       CACHE SIMULATOR RESULTS          {c_reset}")
        lines.append(f"{c_title}========================================{c_reset}")
        
        # 1. Configuration Section
        if config_data:
            lines.append(f"\n{c_header}[System Configuration]{c_reset}")
            # Pretty print the config JSON
            config_str = json.dumps(config_data, indent=2)
            lines.append(config_str)
            lines.append("-" * 40)

        # 2. Statistics Section
        lines.append(f"\n{c_header}[Performance Statistics]{c_reset}")
        
        avg_latency = self.total_latency / self.access_count if self.access_count > 0 else 0
        miss_rate = self.get_miss_rate() * 100
        
        # Access Info
        lines.append(f"{c_label}Total Accesses:{c_reset} {c_val}{self.access_count:<10}{c_reset}")
        lines.append(f"{c_label}Total Hits:    {c_reset} {c_val}{self.hit_count:<10}{c_reset}")
        lines.append(f"{c_label}Total Misses:  {c_reset} {c_warn}{self.miss_count:<10}{c_reset}")
        lines.append(f"{c_label}Miss Rate:     {c_reset} {c_warn if miss_rate > 20 else c_val}{miss_rate:.2f}%{c_reset}")
        
        lines.append("-" * 20)
        
        # Latency Info
        lines.append(f"{c_label}Total Latency: {c_reset} {self.total_latency} cycles")
        lines.append(f"{c_label}Avg Latency:   {c_reset} {avg_latency:.2f} cycles/access")
        
        lines.append("-" * 20)

        # Hierarchy Breakdown
        lines.append(f"{c_label}Access Breakdown per Level:{c_reset}")
        for level_id, count in self.cache_access_count.items():
            lines.append(f"  - {level_id:<10}: {count} accesses")
            
        lines.append("-" * 20)

        # Other metrics
        lines.append(f"{c_label}Total Replacements: {c_reset} {self.replacement_count}")
        lines.append(f"{c_label}Prefetch Count:     {c_reset} {self.prefetch_count}")
        lines.append(f"{c_label}Prefetch Misses:    {c_reset} {self.prefetch_miss_count}")
        prefetch_missrate = self.prefetch_miss_count/self.prefetch_count * 100 if self.prefetch_count != 0 else None
        if prefetch_missrate != None:
            lines.append(f"{c_label}Prefetch Miss Rate: {c_reset} {c_warn if prefetch_missrate > 20 else c_val}{prefetch_missrate:.2f}%{c_reset}")
        
        lines.append(f"{c_title}========================================{c_reset}\n")
        
        return "\n".join(lines)
    
    def print_stats(self):
        """Prints statistics to the terminal with colors."""
        print(self._get_formatted_stats(use_color=True))

    def save_to_file(self, trace_path: str, config_path: str, config_data: dict):
        """
        Saves the statistics and configuration to a file in the output directory.
        Filename format: {trace_name}_{config_name}.txt
        """
        # Extract names for the filename
        trace_name = os.path.splitext(os.path.basename(trace_path))[0]
        config_name = os.path.splitext(os.path.basename(config_path))[0]
        
        output_dir = "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        file_name = f"{trace_name}_{config_name}.txt"
        file_path = os.path.join(output_dir, file_name)
        
        # Get stats without color codes
        content = self._get_formatted_stats(config_data=config_data, use_color=False)
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"{BOLD}{GREEN}Successfully saved detailed report to: {os.path.abspath(file_path)}{RESET}")
        except IOError as e:
            print(f"{BOLD}{RED}Error saving report: {e}{RESET}")