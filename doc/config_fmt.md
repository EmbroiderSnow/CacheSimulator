## **Cache Simulator Configuration File Format (JSON)**

### 1\. Overview

This document specifies the JSON format used to configure the memory hierarchy for the cache simulator. This file defines the properties of each cache level (L1, L2, etc.), the main memory, and the interconnecting buses between them.

The core of the configuration is a JSON object containing three top-level keys:

  * `"cache_hierarchy"`: An **array** of objects, where each object defines a single cache *node*.
  * `"main_memory"`: An object defining the properties of the main memory *node*.
  * `"interconnects"`: An **array** defining the bus properties (like latency) for the *edges* connecting these nodes.

### 2\. Top-Level Structure

```json
{
  "cache_hierarchy": [
    // ... Cache Level 1 Object ...
    // ... Cache Level 2 Object ...
  ],
  "interconnects": [
    // ... Bus Object ...
  ],
  "main_memory": {
    // ... Main Memory Properties ...
  }
}
````

-----

### 3\. `cache_hierarchy` Object Structure

Each object inside the `"cache_hierarchy"` array defines one cache level.

| Key | Type | Description | Required |
| :--- | :--- | :--- | :--- |
| `id` | String | A **unique string identifier** for this level. Used by `"interconnects"` to refer to this node. <br> *Example: "L1-Data", "L2-Unified"* | Yes |
| `level` | Integer | The numerical level (e.g., 1, 2, 3). | Yes |
| `config` | Object | An object containing the specific architectural parameters for this cache level. | Yes |

### 4\. `config` Object Structure (Cache Config)

The `"config"` object specifies the parameters needed to *build* the cache level itself.

| Key | Type | Description | Required |
| :--- | :--- | :--- | :--- |
| `size` | String | The total data capacity of the cache. <br> *Example: "32KB", "256KB", "8MB"* | Yes |
| `associativity` | Integer | The set associativity. | Yes |
| `block_size` | Integer | The size of a single cache line (block) in bytes. <br> *Example: 64* | Yes |
| `replacement_policy` | String | The policy used to select a victim line on a cache miss. <br> *Valid options: "LRU", "SRRIP"* | Yes |
| `prefetch` | Object | Configuration for the prefetcher. See section 4.1 below. | No (Optional) |
| `bypass` | Object | Configuration for the bypass policy. See section 4.2 below. | No (Optional) |
| `hit_latency`| Integer | The time (in cycles) for an access that **hits** in this cache. | Yes |
| `write_policy` | String | The policy for handling store operations. <br> *Valid options: "Write-Back"* | Yes |
| `allocation_policy` | String | The policy for handling write misses. <br> *Valid options: "Write-Allocate"* | Yes |

#### 4.1. `prefetch` Object Structure

If present, this object configures the prefetching strategy for this cache level.

| Key | Type | Description |
| :--- | :--- | :--- |
| `policy_name` | String | The name of the prefetch policy. <br> *Valid options: "NextNLine", "Stream", "Stride", "None"* |
| `degree` | Integer | The number of lines to prefetch (prefetch degree). <br> *Used by: NextNLine, Stream, Stride* |
| `table_size` | Integer | The size of the history table used by the prefetcher. <br> *Used by: Stream, Stride* |

#### 4.2. `bypass` Object Structure

If present, this object configures the cache bypass strategy (deciding whether to insert a line into the cache or bypass it directly to the CPU/next level).

| Key | Type | Description |
| :--- | :--- | :--- |
| `policy_name` | String | The name of the bypass policy. <br> *Valid options: "Prob" (Probabilistic), "NoBypass"* |
| `bypass_prob_demand` | Float | The probability (0.0 to 1.0) of bypassing a **demand** (read/write) request. <br> *Used by: Prob* |
| `bypass_prob_prefetch` | Float | The probability (0.0 to 1.0) of bypassing a **prefetch** request. <br> *Used by: Prob* |

-----

### 5\. `interconnects` Object Structure

This array defines the "wires" connecting the components.

| Key | Type | Description | Required |
| :--- | :--- | :--- | :--- |
| `from` | String | The `id` of the source component. Use **"CPU"** for the connection to the first-level cache. | Yes |
| `to` | String | The `id` of the destination component. Use **"MainMemory"** for the connection to main memory. | Yes |
| `bus_latency` | Integer | The round-trip time (in cycles) for a request/response over this bus. | Yes |

-----

### 6\. `main_memory` Object Structure

The `"main_memory"` object defines the final backing store.

| Key | Type | Description | Required |
| :--- | :--- | :--- | :--- |
| `access_latency` | Integer | The fixed latency (in cycles) for an access that reaches main memory. | Yes |

-----

### 7\. Complete Example

This example defines a two-level cache hierarchy. L1 uses a simple "NextNLine" prefetcher, while L2 uses a complex "Stride" prefetcher, "SRRIP" replacement, and probabilistic bypassing.

```json
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
          "degree": 4
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
        "prefetch": {
          "policy_name": "Stride",
          "degree": 8,
          "table_size": 16 
        },
        "bypass": {
          "policy_name": "Prob",
          "bypass_prob_demand": 0.05,
          "bypass_prob_prefetch": 0.1
        },
        "hit_latency": 10,
        "write_policy": "Write-Back",
        "allocation_policy": "Write-Allocate"
      }
    }
  ],
  "interconnects": [
    {
      "from": "CPU",
      "to": "L1-Cache",
      "bus_latency": 0 
    },
    {
      "from": "L1-Cache",
      "to": "L2-Cache",
      "bus_latency": 6
    },
    {
      "from": "L2-Cache",
      "to": "MainMemory",
      "bus_latency": 0
    }
  ],
  "main_memory": {
    "access_latency": 100
  }
}
```
