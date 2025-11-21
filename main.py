import argparse
from cache_simulator.controller.control import MemoryController

def main():
    parser = argparse.ArgumentParser(description="Cache Simulator")
    parser.add_argument("--config", type=str, required=True, help="Path to the cache configuration JSON file")
    parser.add_argument("--trace", type=str, required=True, help="Path to the memory access trace file")
    args = parser.parse_args()

    controller = MemoryController(args.config)
    run_simulation(controller, args.trace)

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
    controller.performance.print_stats()

if __name__ == "__main__":
    main()
