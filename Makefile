# Makefile for Cache Simulator Experiments

PYTHON = python3
SIM_SCRIPT = main.py

# Trace files
TRACE_MCF = traces/01-mcf-gem5-xcg.trace
TRACE_STREAM = traces/02-stream-gem5-xaa.trace
TRACES = $(TRACE_MCF) $(TRACE_STREAM)

# Configuration files
CONFIG_BASELINE = config/exp_baseline.json
CONFIG_SRRIP = config/exp_srrip.json
CONFIG_PREFETCH_NEXT = config/exp_prefetch_nextline.json
CONFIG_PREFETCH_STRIDE = config/exp_prefetch_stride.json
CONFIG_BYPASS = config/exp_bypass.json
CONFIG_OPTIMAL = config/exp_optimal.json

# Output directory (Results will be saved here automatically by the updated python script)
OUTPUT_DIR = output

.PHONY: all clean baseline srrip prefetch bypass optimal help

# Default target: run all experiments
all: baseline srrip prefetch bypass optimal
	@echo "All experiments completed. Check the '$(OUTPUT_DIR)' directory for results."

# 1. Baseline Experiment
baseline:
	@echo ">>> Running Baseline Experiments..."
	@for trace in $(TRACES); do \
		echo "Running Baseline on $$trace"; \
		$(PYTHON) $(SIM_SCRIPT) --config $(CONFIG_BASELINE) --trace $$trace; \
	done

# 2. SRRIP Replacement Policy Experiment
srrip:
	@echo ">>> Running SRRIP Experiments..."
	@for trace in $(TRACES); do \
		echo "Running SRRIP on $$trace"; \
		$(PYTHON) $(SIM_SCRIPT) --config $(CONFIG_SRRIP) --trace $$trace; \
	done

# 3. Prefetch Experiments (NextLine & Stride)
prefetch:
	@echo ">>> Running Prefetch Experiments (NextNLine)..."
	@for trace in $(TRACES); do \
		echo "Running NextNLine on $$trace"; \
		$(PYTHON) $(SIM_SCRIPT) --config $(CONFIG_PREFETCH_NEXT) --trace $$trace; \
	done
	@echo ">>> Running Prefetch Experiments (Stride)..."
	@for trace in $(TRACES); do \
		echo "Running Stride on $$trace"; \
		$(PYTHON) $(SIM_SCRIPT) --config $(CONFIG_PREFETCH_STRIDE) --trace $$trace; \
	done

# 4. Bypass Experiment
bypass:
	@echo ">>> Running Bypass Experiments..."
	@for trace in $(TRACES); do \
		echo "Running Bypass on $$trace"; \
		$(PYTHON) $(SIM_SCRIPT) --config $(CONFIG_BYPASS) --trace $$trace; \
	done

# 5. Optimal Combination Experiment
optimal:
	@echo ">>> Running Optimal Combination Experiments..."
	@for trace in $(TRACES); do \
		echo "Running Optimal on $$trace"; \
		$(PYTHON) $(SIM_SCRIPT) --config $(CONFIG_OPTIMAL) --trace $$trace; \
	done

# Clean output directory
clean:
	rm -rf $(OUTPUT_DIR)
	@echo "Output directory cleaned."

help:
	@echo "Available targets:"
	@echo "  all       : Run all experiments (Baseline, SRRIP, Prefetch, Bypass, Optimal)"
	@echo "  baseline  : Run only baseline experiments"
	@echo "  srrip     : Run only SRRIP replacement policy experiments"
	@echo "  prefetch  : Run only prefetching experiments (NextLine & Stride)"
	@echo "  bypass    : Run only bypass experiments"
	@echo "  optimal   : Run the combined optimal configuration"
	@echo "  clean     : Remove the output directory"