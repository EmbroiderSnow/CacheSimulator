## **Cache Simulator Configuration File Format (JSON)**

### 1\. Overview

This document specifies the JSON format used to configure the memory hierarchy for the cache simulator. This file defines the properties of each cache level (L1, L2, etc.), the main memory, and the interconnecting buses between them.

The core of the configuration is a JSON object containing three top-level keys:

  * `"cache_hierarchy"`: An **array** of objects, where each object defines a single cache *node*.
  * `"main_memory"`: An object defining the properties of the main memory *node*.
  * `"interconnects"`: An **array** defining the bus properties (like latency) for the *edges* connecting these nodes. This section is used by the Control Plane.

### 2\. Top-Level Structure

```json
{
  "cache_hierarchy": [
    // ... Cache Level 1 Object ...
    // ... Cache Level 2 Object ...
    // ... etc. ...
  ],
  "interconnects": [
    // ... Bus Object (e.g., CPU to L1) ...
    // ... Bus Object (e.g., L1 to L2) ...
    // ... Bus Object (e.g., L2 to Main Memory) ...
  ],
  "main_memory": {
    // ... Main Memory Properties ...
  }
}
```

-----

### 3\. `cache_hierarchy` Object Structure

Each object inside the `"cache_hierarchy"` array defines one cache level.

| Key | Type | Description | Required |
| :--- | :--- | :--- | :--- |
| `id` | String | A **unique string identifier** for this level. Used by `"interconnects"` to refer to this node. <br> *Example: "L1-Data", "L2-Unified", "L3"* | Yes |
| `level` | Integer | The numerical level (e.g., 1, 2, 3). Used for logging. | Yes |
| `config` | Object | An object containing the specific architectural parameters for this cache level. | Yes |

### 4\. `config` Object Structure (Cache Config)

The `"config"` object specifies the parameters needed to *build* the cache level itself.

| Key | Type | Description | Required |
| :--- | :--- | :--- | :--- |
| `size` | String | The total data capacity of the cache. <br> *Example: "32KB", "256KB", "8MB"* | Yes |
| `associativity` | Integer | The set associativity. | Yes |
| `block_size` | Integer | The size of a single cache line (block) in bytes. <br> *Example: 64* | Yes |
| `replacement_policy` | String | The policy used to select a victim line on a cache miss. <br> *Valid options: "LRU", "FIFO"* | Yes |
| `hit_latency`| Integer | The time (in cycles) for an access that **hits** in this cache. This represents the internal lookup and data retrieval time. | Yes |
| `write_policy` | String | The policy for handling store operations. <br> *Valid options: "Write-Back"* | Yes |
| `allocation_policy` | String | The policy for handling write misses. <br> *Valid options: "Write-Allocate", "No-Write-Allocate"* | Yes |

-----

### 5\. `interconnects` Object Structure

This array defines the "wires" connecting the components. The `CacheController` reads this section to understand the hierarchy's topology and timing.

| Key | Type | Description | Required |
| :--- | :--- | :--- | :--- |
| `from` | String | The `id` of the source component. Use the special string **"CPU"** for the connection to the first-level cache. | Yes |
| `to` | String | The `id` of the destination component. Use the special string **"MainMemory"** for the connection to main memory. | Yes |
| `bus_latency` | Integer | The round-trip time (in cycles) for a request/response over this bus. | Yes |

-----

### 6\. `main_memory` Object Structure

The `"main_memory"` object defines the final backing store.

| Key | Type | Description | Required |
| :--- | :--- | :--- | :--- |
| `access_latency` | Integer | The fixed latency (in cycles) for an access that reaches main memory. This represents the internal DRAM access time, *after* the final bus latency has been paid. | Yes |

-----

### 7\. Latency Calculation Model

The simulator's `CacheController` uses this entire configuration to calculate total latency.

  * **Scenario 1: L1 Hit** (Assuming `L1.id = "L1"`)

      * The request is checked against the "L1" cache and hits.
      * `Total Latency = L1.config.hit_latency`
      * *Example: `4` cycles.*

  * **Scenario 2: L1 Miss, L2 Hit** (Assuming `L1.id = "L1"`, `L2.id = "L2"`)

      * 1.  Pay L1 hit latency to discover the miss.
      * 2.  Find the interconnect `where from == "L1" and to == "L2"`. Pay its `bus_latency`.
      * 3.  Pay L2 hit latency to find the data in L2.
      * `Total Latency = L1.config.hit_latency + Interconnect(L1 $\to$ L2).bus_latency + L2.config.hit_latency`
      * *Example: `4 + 2 + 10 = 16` cycles.*

  * **Scenario 3: L1 Miss, L2 Miss, Main Memory Hit**

      * `Total Latency = L1.config.hit_latency + Interconnect(L1 $\to$ L2).bus_latency + L2.config.hit_latency + Interconnect(L2 $\to$ Mem).bus_latency + MainMemory.access_latency`
      * *Example: `4 + 2 + 10 + 20 + 100 = 136` cycles.*

-----

### 8\. Complete Example

This example defines a two-level cache hierarchy using the `interconnects` model.

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
        "replacement_policy": "LRU",
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
      "bus_latency": 1 
    },
    {
      "from": "L1-Cache",
      "to": "L2-Cache",
      "bus_latency": 2
    },
    {
      "from": "L2-Cache",
      "to": "MainMemory",
      "bus_latency": 20
    }
  ],
  "main_memory": {
    "access_latency": 100
  }
}
```