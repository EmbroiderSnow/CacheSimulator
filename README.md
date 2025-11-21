# Cache Simulator

This project is a flexible, event-driven cache simulator designed to model a multi-level memory hierarchy. It reads a JSON configuration file to define the architecture (e.g., L1/L2 cache properties, bus latencies, main memory latency) and processes a memory access trace file to simulate read and write operations. At the end of the simulation, it prints detailed performance statistics.

## Features

  * **Multi-Level Hierarchy:** Simulate complex memory hierarchies with any number of cache levels (L1, L2, L3, etc.).
  * **Dynamic Configuration:** Define all cache parameters via an external JSON file, including:
      * Cache size, associativity, and block size.
      * **Replacement Policies:** Supports **LRU** (Least Recently Used) and **SRRIP** (Static Re-reference Interval Prediction).
      * **Prefetching:** Supports various prefetch strategies including **NextNLine**, **Stream**, and **Stride** prefetchers with configurable degrees and table sizes.
      * **Bypassing:** Supports probabilistic bypassing for demand and prefetch requests.
      * Write policies (Write-Back) and allocation policies (Write-Allocate).
  * **Detailed Latency Model:** Accurately models latencies for cache hits, bus transfers between levels, and main memory access.
  * **Performance Tracking:** Reports key statistics, including total accesses, hit/miss counts, prefetch metrics, and total latency, to evaluate the hierarchy's performance.

## Requirements

  * Python 3.x

The simulator uses standard Python libraries (`argparse`, `json`) and requires no external dependencies.

## How to Run

The simulator is run from the command line, requiring two arguments: a path to the configuration file and a path to the trace file.

### Command

```bash
python main.py --config <path_to_config_json> --trace <path_to_trace_file>
```

Example

Using the provided configuration and trace files:

```bash
python main.py --config config/config.json --trace traces/trace1.txt
```

Trace File Format

The trace file must be a plain text file where each line represents one memory access. The format for each line is:

```
<operation> <address>
```

- \<operation>: A single character, either r for a read or w for a write.

- \<address>: The memory address for the operation, represented in hexadecimal format (e.g., 0x1a2b3c4d).

Example (traces/trace1.txt):

```
r 0x1000
w 0x1008
r 0x2000
...
```

Configuration File Format

The entire memory hierarchy is defined by a single JSON file. This file has three top-level keys: cache_hierarchy, interconnects, and main_memory.

See doc/config_fmt.md for a complete specification.

1. cache_hierarchy

    An array of objects, where each object defines one level of the cache.

    - id: A unique string name (e.g., "L1-Cache").

    - level: The numerical level (e.g., 1).

    - config: An object containing the cache's architectural parameters:

      - size: Total data capacity (e.g., "32KB").

      - associativity: Set associativity (e.g., 8).

      - block_size: Size of a cache line in bytes (e.g., 64).

      - replacement_policy: "LRU" or "SRRIP".

      - prefetch: (Optional) Object defining prefetch policy (e.g., "NextNLine", "Stride") and parameters.

      - bypass: (Optional) Object defining bypass policy (e.g., "Prob").

      - hit_latency: Time in cycles for a cache hit.

      - write_policy: "Write-Back".

      - allocation_policy: "Write-Allocate".

2. interconnects

    An array defining the "wires" connecting the components.

      - from: The id of the source (use "CPU" for the connection to L1).

      - to: The id of the destination (use "MainMemory" for the connection to memory).

      - bus_latency: The round-trip time in cycles for this connection.

3. main_memory

    An object defining the final backing store.

    - access_latency: The fixed time in cycles to access main memory, after the final bus latency is paid.

Example (config/baseline.json)

```JSON

{
  "cache_hierarchy": [
    {
      "id": "L1-Cache",
      "level": 1,
      "config": {
        "size": "32KB",
        "associativity": 8,
        "block_size": 64,
        "replacement_policy": "LRU",
        "prefetch": {
          "policy_name": "NextNLine",
          "degree": 2
        },
        "hit_latency": 4,
        "write_policy": "Write-Back",
        "allocation_policy": "Write-Allocate"
      }
    },
    {
      "id": "L2-Cache",
      "level": 2,
      "config": {
        "size": "256KB",
        "associativity": 8,
        "block_size": 64,
        "replacement_policy": "SRRIP",
        "hit_latency": 10,
        "write_policy": "Write-Back",
        "allocation_policy": "Write-Allocate"
      }
    }
  ],
  "interconnects": [
    { "from": "CPU", "to": "L1-Cache", "bus_latency": 0 },
    { "from": "L1-Cache", "to": "L2-Cache", "bus_latency": 6 },
    { "from": "L2-Cache", "to": "MainMemory", "bus_latency": 0 }
  ],
  "main_memory": {
    "access_latency": 100
  }
}
```

Project Architecture

The simulator is structured into several key components:

- main.py: The main entry point. It uses argparse to get the config and trace file paths. It initializes the MemoryController and then reads the trace file line by line, calling controller.read() or controller.write() for each operation. Finally, it calls controller.performance.print_stats() to output the results.

- cache_simulator/controller/: This package contains the high-level simulation logic.

    - control.py (MemoryController): This is the "brain" of the simulator. It orchestrates the access flow, latencies, and statistics.

    - memoryHierarchy.py (MemoryHierarchy): Parses the JSON configuration and builds the Cache objects.

    - performance.py (Performance): Tracks performance metrics (hits, misses, latency, replacements, prefetch stats).

- cache_simulator/memory/: This package contains the core data structures for the cache itself.

    - cache.py (Cache): Represents a single cache level.

    - set.py (Set): Represents a single set within a cache.

    - line.py (Line): Represents a single cache line.

- cache_simulator/policy/: This package implements the swappable policies.

    - Eviction: LRU, SRRIP.

    - Prefetch: NextNLine, Stream, Stride.

    - Bypass: Prob (Probabilistic).

## Latency Calculation Model

The total latency for an access is calculated based on the path taken through the hierarchy. This model is specified in `doc/config_fmt.md`.

  * **Scenario 1: L1 Hit**

      * `Total Latency = L1.config.hit_latency`
      * *Example: `4` cycles*.

  * **Scenario 2: L1 Miss, L2 Hit**

      * `Total Latency = L1.hit_latency + Interconnect(L1->L2).bus_latency + L2.hit_latency`
      * *Example: `4 + 2 + 10 = 16` cycles*.

  * **Scenario 3: L1 Miss, L2 Miss, Main Memory Hit**

      * `Total Latency = L1.hit_latency + Interconnect(L1->L2).bus_latency + L2.hit_latency + Interconnect(L2->Mem).bus_latency + MainMemory.access_latency`
      * *Example: `4 + 2 + 10 + 20 + 100 = 136` cycles*.

This latency is aggregated by the `MemoryController` during the `read()` operation.