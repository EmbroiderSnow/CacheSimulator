import argparse
import json
import os
from cache_simulator.controller.control import MemoryController

def main():
    parser = argparse.ArgumentParser(description="Cache Simulator")
    parser.add_argument("--config", type=str, required=True, help="Path to the cache configuration JSON file")
    parser.add_argument("--trace", type=str, required=True, help="Path to the memory access trace file")
    args = parser.parse_args()

    # Initialize Controller
    controller = MemoryController(args.config)
    
    # Run Simulation
    run_simulation(controller, args.trace)

    # Load configuration data for reporting
    config_data = {}
    try:
        with open(args.config, 'r') as f:
            config_data = json.load(f)
    except Exception as e:
        print(f"Warning: Could not read config file for report: {e}")

    # Output Results
    # 1. Print to Terminal (Beautified)
    controller.performance.print_stats()
    
    # 2. Save to File
    controller.performance.save_to_file(args.trace, args.config, config_data)

def run_simulation(controller: MemoryController, trace_file: str):
    with open(trace_file, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) != 2:
                continue
            operation, address_str = parts
            address = int(address_str, 16)

            if operation == 'r':
                controller.read(address)
            elif operation == 'w':
                controller.write(address)
            else:
                print(f"Unknown operation: {operation}")

    controller.collect_prefetch_information()
    # Note: print_stats call is moved to main() to handle config data passing better

if __name__ == "__main__":
    main()